import replicate
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from datetime import datetime

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def convert_audio_to_text(file_path):
    model = replicate.Client(api_token=REPLICATE_API_TOKEN)
    try:
        # Run speech recognition model with audio file as a file parameter
        with open(file_path, "rb") as audio_file:
            output = model.run(
                "openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
                input={"audio": audio_file}
            )

        # Extract and return text from output
        text = output["segments"][0]["text"]
        return text
    except (FileNotFoundError, ValidationError, KeyError, replicate.exceptions.ReplicateError) as e:
        # Handle file or data validation errors
        return f"Error processing audio: {e}"
