# Description: This file contains the function that converts text to speech using the Deepgram API.
import requests
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from io import BytesIO
from config import API_KEY, TEXT_FILE


def text_to_speech(text): # method to convert text to speech


    url = "https://api.deepgram.com/v1/speak?model=aura-arcas-en" # Deepgram API URL

    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = { # payload to send to the API, replaced with the text to be converted
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload) # send the request to the API

    if response.status_code == 200: # check if the response is successful

        audio_segment = AudioSegment.from_file(BytesIO(response.content), format="mp3") # convert the audio to a segment

        raw_audio = np.array(audio_segment.get_array_of_samples()) # get the raw audio data

        sd.play(raw_audio, samplerate=audio_segment.frame_rate) # play the audio

        sd.wait()

        print(text)
        print("Audio played successfully.")

    else:
        print(f"Error: {response.status_code} - {response.text}")


