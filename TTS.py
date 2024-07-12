import requests
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from io import BytesIO
from config import API_KEY, TEXT_FILE


def text_to_speech(text): # event
    with open(TEXT_FILE, "a") as file:
        file.write(text + "\n")

    url = "https://api.deepgram.com/v1/speak?model=aura-helios-en"

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:

        audio_segment = AudioSegment.from_file(BytesIO(response.content), format="mp3")

        raw_audio = np.array(audio_segment.get_array_of_samples())

        sd.play(raw_audio, samplerate=audio_segment.frame_rate)

        sd.wait()

        print(text)
        print("Audio played successfully.")
        file.close()
    else:
        print(f"Error: {response.status_code} - {response.text}")


