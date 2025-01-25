from flask import Flask, request, jsonify
from pathlib import Path
import json
import os
import sys
from ZEGGS.generate import generate_gesture
import torch
from dotenv import load_dotenv


app = Flask(__name__)

# Default paths and configs
PROJECT_PATH = Path(__file__).parent.parent #Path("B:/Developer/Projects/TextToVideo/ThirdParty/ZeroEGGS")
NETWORK_PATH = PROJECT_PATH / "data/outputs/v1/saved_models"
DATA_PATH = PROJECT_PATH / "data/processed_v1"
STYLES_PATH = PROJECT_PATH / "data/clean"
RESULTS_PATH = PROJECT_PATH / "results"

# Add local sox to PATH
SOX_PATH = str(PROJECT_PATH / "third_party" / "sox")
os.environ["PATH"] = SOX_PATH + os.pathsep + os.environ["PATH"]
sys.path.append(SOX_PATH)

print(SOX_PATH)

# Load configuration once
with open(PROJECT_PATH / "configs/configs_v1.json", "r") as f:
    DEFAULT_CONFIG = json.load(f)


@app.route("/generate", methods=["POST"])
def generate_animation():
    try:
        data = request.get_json()

        # Required parameters
        audio_file = Path(data["audio_file"])
        styles = [(Path(STYLES_PATH / style[0]), style[1]) for style in data["styles"]]
        print(f"Processed styles: {styles}")


        # Optional parameters
        style_encoding_type = data.get("style_encoding_type", "example")
        blend_type = data.get("blend_type", "add")
        blend_ratio = data.get("blend_ratio", [0.5, 0.5])
        file_name = data.get("file_name", None)
        temperature = data.get("temperature", 1.0)
        seed = data.get("seed", 1234)
        use_gpu = data.get("use_gpu", torch.cuda.is_available())



        # Generate animation
        result = generate_gesture(
            audio_file=audio_file,
            styles=styles,
            network_path=NETWORK_PATH,
            data_path=DATA_PATH,
            results_path=RESULTS_PATH,
            style_encoding_type=style_encoding_type,
            blend_type=blend_type,
            blend_ratio=blend_ratio,
            file_name=file_name,
            temperature=temperature,
            seed=seed,
            use_gpu=use_gpu
        )

        # Return path to generated animation
        output_path = str(RESULTS_PATH / f"{file_name}.bvh" if file_name else RESULTS_PATH / "generated.bvh")
        return jsonify({
            "status": "success",
            "animation_path": output_path #,
            #"style_encoding": result.tolist() if isinstance(result, torch.Tensor) else result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    load_dotenv()
    host = os.getenv('SERVER_HOST', '127.0.0.1')
    port = int(os.getenv('SERVER_PORT', 5003))
    app.run(host=host, port=port, debug=False)