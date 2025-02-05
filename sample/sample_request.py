import requests

url = "http://localhost:5003/generate"
data = {
    #"audio_file": "B:/Developer/Projects/TextToVideo/TextToVideo/Saved/Audio/audio_20250124_182641.wav",
    "audio_file": "B:/Developer/Projects/TextToVideo/sss-unreal/Saved/Audio/audio_20250205_153259.wav",
    "emotion": "happy",
    "file_name": "audio_20250205_153259"
}
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")