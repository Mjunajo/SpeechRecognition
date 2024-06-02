import replicate
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from datetime import datetime

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

class SpeechInput(BaseModel):
    audio: bytes

class Prediction(BaseModel):
    output: str
    started_at: str = datetime.now().isoformat()
    completed_at: str = datetime.now().isoformat()

def convert_audio_to_text(file_path):
    model = replicate.Client(api_token=REPLICATE_API_TOKEN)
    try:
        # Read audio file as bytes
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Create input data object
        input_data = SpeechInput(audio=audio_data)

        # Run speech recognition model
        output = model.run(
            "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
            input=input_data.dict()
        )

        # Extract and return text from output
        text = output["segments"][0]["text"]
        return text
    except (FileNotFoundError, ValidationError, KeyError) as e:
        # Handle file or data validation errors
        return f"Error processing audio: {e}"
