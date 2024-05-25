import os
import replicate
from pydub import AudioSegment
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def recognize_speech_from_audio(audio_file_path):
    # Ensure API token is set
    replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
    if not replicate_api_token:
        raise ValueError("Replicate API token not set")

    # Set the Replicate API token
    client = replicate.Client(api_token=replicate_api_token)

    # Convert MP3 to WAV if necessary
    if audio_file_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_file_path)
        audio_file_path = audio_file_path.replace('.mp3', '.wav')
        audio.export(audio_file_path, format='wav')

    # Upload audio file to Replicate
    try:
        with open(audio_file_path, 'rb') as f:
            model_input = {"audio": f}
            prediction = client.predictions.create(
                version="openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
                input=model_input
            )
    except Exception as e:
        logging.error(f"Error uploading audio file to Replicate: {e}")
        return "Could not transcribe the audio"

    # Log the entire prediction object for debugging
    logging.debug(f"Prediction object: {prediction}")

    # Handle response
    if not hasattr(prediction, 'status'):
        logging.warning("Response object does not have 'status' attribute")
        logging.warning(f"Response content: {prediction}")
        return "Could not transcribe the audio"

    if prediction.status == "succeeded":
        if hasattr(prediction, 'output') and isinstance(prediction.output, dict) and "segments" in prediction.output:
            transcription = " ".join([segment["text"] for segment in prediction.output["segments"]])
            return transcription
        else:
            logging.warning("Output is missing or not in expected format")
            logging.warning(f"Output content: {prediction.output}")
            return "Could not transcribe the audio"
    elif prediction.status == "failed":
        if hasattr(prediction, 'error'):
            logging.error(f"Prediction failed with error: {prediction.error}")
            return "Could not transcribe the audio"
        else:
            logging.warning("Prediction failed without an error message")
            return "Could not transcribe the audio"
    else:
        logging.warning("Unexpected response status from Replicate API")
        logging.warning(f"Response content: {prediction}")
        return "Could not transcribe the audio"

# Example usage (for testing)
if __name__ == "__main__":
    audio_path = "path_to_your_audio_file.mp3"  # Replace with your audio file path
    print(recognize_speech_from_audio(audio_path))
