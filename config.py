# Configuration settings for the project

from dotenv import load_dotenv
import os


load_dotenv()

# API key for Deepgram
API_KEY = os.getenv("DG_API_KEY")

# File path for saving the final transcript
TEXT_FILE = "final_transcript.txt"