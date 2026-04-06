# Install the requests package by executing the command "pip install requests"

import requests
import time

base_url = "https://api.assemblyai.com"

headers = {"authorization": ""}

with open("./audio.mp3", "rb") as f:
    response = requests.post(base_url + "/v2/upload", headers=headers, data=f)

audio_url = response.json()["upload_url"]


data = {
    "audio_url": audio_url,
    "language_detection": True,
    "speech_models": ["universal-3-pro", "universal-2"],
}

url = base_url + "/v2/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()["id"]
polling_endpoint = base_url + "/v2/transcript/" + transcript_id

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()
    transcript_text = transcription_result["text"]

    if transcription_result["status"] == "completed":
        print(f"Transcript Text:", transcript_text)
        break

    elif transcription_result["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

    else:
        time.sleep(3)
