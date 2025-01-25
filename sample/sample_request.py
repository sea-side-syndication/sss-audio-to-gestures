import requests

url = "http://localhost:5003/generate"
data = {
    #"audio_file": "B:/Developer/Projects/TextToVideo/TextToVideo/Saved/Audio/audio_20250124_182641.wav",
    "audio_file": "B:/Developer/Projects/TextToVideo/TextToVideo/Saved/Audio/Sample2.wav",
    "styles": [("067_Speech_2_x_1_0.bvh", [0, 100])],  # List containing one [file, range] pair
    "file_name": "my_animation"
}
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")