# speech_recognizer.py
import replicate
import os
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def convert_audio_to_text(file_path):
    model = replicate.Client(api_token=REPLICATE_API_TOKEN)
    input = {"audio": open(file_path, "rb")}
    output = model.run(
        "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
        input=input
    )
    return output["segments"][0]["text"]
