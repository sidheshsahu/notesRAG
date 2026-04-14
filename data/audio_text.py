import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("ASSEMBLYAI_API_KEY")


def transcribe_audio(file_path):
    base_url = "https://api.assemblyai.com"

    headers = {"authorization": api_key}

    with open(file_path, "rb") as f:
        response = requests.post(base_url + "/v2/upload", headers=headers, data=f)

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url,
        "speech_models": ["universal-3-pro", "universal-2"],
        "language_detection": True,
        "speaker_labels": True,
    }

    url = base_url + "/v2/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()["id"]
    polling_endpoint = base_url + "/v2/transcript/" + transcript_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result["status"] == "completed":
            break

        elif transcription_result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

    final_text = ""

    for utterance in transcription_result["utterances"]:
        final_text += f"Speaker {utterance['speaker']}: {utterance['text']}\n"

    return final_text


print(transcribe_audio(r"D:\notesRAG\notesRAG\speech.mp3"))
