from ZEGGS.emotion_styles import get_random_style_for_emotion, Emotion
from ZEGGS.generate import generate_gesture

from ZEGGS.utility.logger import logger

from flask import Flask, request, jsonify
from pathlib import Path
import json
import os
import sys
import logging
from typing import Optional, Dict, Tuple, Union, Any

import torch
from dotenv import load_dotenv


app = Flask(__name__)

# Default paths and configs
PROJECT_PATH = Path(__file__).parent.parent
NETWORK_PATH = PROJECT_PATH / "data/outputs/v1/saved_models"
DATA_PATH = PROJECT_PATH / "data/processed_v1"
STYLES_PATH = PROJECT_PATH / "data/clean"
RESULTS_PATH = PROJECT_PATH / "results"

# Ensure required directories exist
RESULTS_PATH.mkdir(parents=True, exist_ok=True)


def validate_style_file(style_path: Path) -> bool:
    """Validate that a style file exists and is a valid BVH file."""
    try:
        if not style_path.exists():
            logger.error(f"Style file does not exist: {style_path}")
            return False
        if style_path.suffix.lower() != '.bvh':
            logger.error(f"Style file is not a BVH file: {style_path}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error validating style file: {e}")
        return False


def initialize_sox():
    """Initialize SOX and handle missing SOX gracefully."""
    sox_path = PROJECT_PATH / "third_party" / "sox"

    if not sox_path.exists():
        logger.warning(f"SOX directory not found at {sox_path}")
        return False

    # Add SOX to PATH
    os.environ["PATH"] = str(sox_path) + os.pathsep + os.environ["PATH"]

    # Test SOX availability
    import subprocess
    try:
        subprocess.run(['sox', '--version'], capture_output=True, text=True)
        logger.info("SOX initialized successfully")
        return True
    except FileNotFoundError:
        logger.error("""
        SOX could not be found! Please ensure SOX is installed:
        1. Download from http://sox.sourceforge.net/
        2. Place in third_party/sox directory
        3. Ensure sox.exe is present
        """)
        return False


# Initialize SOX (but don't fail if it's not available)
SOX_AVAILABLE = initialize_sox()

# Load configuration once at startup
try:
    with open(PROJECT_PATH / "configs/configs_v1.json", "r") as f:
        DEFAULT_CONFIG = json.load(f)
except FileNotFoundError as e:
    logger.error(f"Failed to load config file: {e}")
    DEFAULT_CONFIG = {}


def validate_paths() -> bool:
    """Validate that all required paths and files exist."""
    required_paths = [
        (NETWORK_PATH, "Network path"),
        (DATA_PATH, "Data path"),
        (STYLES_PATH, "Styles path")
    ]

    for path, name in required_paths:
        if not path.exists():
            logger.error(f"{name} does not exist: {path}")
            return False

    # Check if required network files exist
    required_files = [
        NETWORK_PATH / "speech_encoder.pt",
        NETWORK_PATH / "decoder.pt",
        NETWORK_PATH / "style_encoder.pt",
        DATA_PATH / "stats.npz",
        DATA_PATH / "data_definition.json",
        DATA_PATH / "data_pipeline_conf.json"
    ]

    for file_path in required_files:
        if not file_path.exists():
            logger.error(f"Required file not found: {file_path}")
            return False

    return True


def process_request(data: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[int]]:
    """Process the request data and validate inputs."""
    try:
        # Required parameters
        audio_file = Path(data["audio_file"])
        if not audio_file.exists():
            return {"status": "error", "message": f"Audio file not found: {audio_file}"}, 400

        if not SOX_AVAILABLE:
            return {"status": "error", "message": "SOX is not available. Audio processing cannot proceed."}, 500

        # Get emotion and style
        emotion_str = data.get("emotion", "neutral").lower()
        try:
            emotion = Emotion(emotion_str)
            style_file = get_random_style_for_emotion(emotion)
            style_path = STYLES_PATH / style_file

            # Validate style file
            if not validate_style_file(style_path):
                return {"status": "error", "message": f"Invalid or missing style file: {style_path}"}, 500

            logger.info(f"Using style file: {style_path}")
            styles = [(style_path, [0, 100])]

        except ValueError as e:
            logger.error('exception:',str(e) )
            return {"status": "error", "message": f"Invalid emotion: {emotion_str}"}, 400

        # Optional parameters with defaults
        params = {
            "style_encoding_type": data.get("style_encoding_type", "example"),
            "blend_type": data.get("blend_type", "add"),
            "blend_ratio": data.get("blend_ratio", [0.5, 0.5]),
            "file_name": data.get("file_name", audio_file.stem + "_" + emotion_str),
            "temperature": float(data.get("temperature", 1.0)),
            "seed": int(data.get("seed", 1234)),
            "use_gpu": bool(data.get("use_gpu", torch.cuda.is_available()))
        }

        return {
            "audio_file": audio_file,
            "styles": styles,
            "emotion": emotion,
            **params
        }, None

    except KeyError as e:
        logger.exception("Error processing request", str(e))
        return {"status": "error", "message": f"Missing required parameter: {str(e)}"}, 400
    except Exception as e:
        logger.exception("Error processing request", str(e))
        return {"status": "error", "message": f"Error processing request: {str(e)}"}, 400


@app.route("/generate", methods=["POST"])
def generate_animation():
    """Generate an animation from audio using ZEGGS."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        logger.info(f"Received request: {data}")

        # Validate paths first
        if not validate_paths():
            return jsonify({"status": "error", "message": "Server configuration error"}), 500

        # Process and validate request data
        processed_data, error = process_request(data)
        if error:
            return jsonify(processed_data), error

        logger.info(f"Using style path: {processed_data['styles'][0][0]}")

        # Generate animation
        result = generate_gesture(
            audio_file=processed_data["audio_file"],
            styles=processed_data["styles"],
            network_path=NETWORK_PATH,
            data_path=DATA_PATH,
            results_path=RESULTS_PATH,
            style_encoding_type=processed_data["style_encoding_type"],
            blend_type=processed_data["blend_type"],
            blend_ratio=processed_data["blend_ratio"],
            file_name=processed_data["file_name"],
            temperature=processed_data["temperature"],
            seed=processed_data["seed"],
            use_gpu=processed_data["use_gpu"]
        )

        output_path = RESULTS_PATH / f"{processed_data['file_name']}.bvh"

        return jsonify({
            "status": "success",
            "animation_path": str(output_path),
            "emotion": processed_data["emotion"].value,
            "style_used": str(processed_data["styles"][0][0])
        })

    except Exception as e:
        logger.exception("Error processing request", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    status = {
        "paths_valid": validate_paths(),
        "sox_available": SOX_AVAILABLE,
        "styles_present": list(STYLES_PATH.glob('*.bvh')) if STYLES_PATH.exists() else [],
        "overall_status": "healthy" if (validate_paths() and SOX_AVAILABLE) else "unhealthy"
    }
    return jsonify(status)

def run():
    load_dotenv()
    host = os.getenv('SERVER_HOST', '127.0.0.1')
    port = int(os.getenv('SERVER_PORT', 5003))

    # Validate paths on startup
    if not validate_paths():
        logger.error("Failed to validate required paths. Please check configuration.")
        sys.exit(1)

    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    run()