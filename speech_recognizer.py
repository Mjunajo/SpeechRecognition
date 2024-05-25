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
    with open(audio_file_path, 'rb') as f:
        model_input = {"audio": f}
        prediction = client.predictions.create(
            version="openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2",
            input=model_input
        )

    # Log the entire prediction object for debugging
    logging.debug(f"Prediction object: {prediction}")

    # Ensure the prediction object is a dictionary
    if isinstance(prediction, str):
        logging.warning("Received a string object instead of a prediction object")
        logging.warning(f"Response content: {prediction}")
        return "Could not transcribe the audio"

    if not isinstance(prediction, dict):
        logging.error("Prediction object is not a dictionary")
        logging.error(f"Unexpected response type: {type(prediction)}")
        logging.error(f"Response content: {prediction}")
        return "Could not transcribe the audio"

    # Handle response
    status = prediction.get('status')
    if not status:
        logging.warning("Response object does not have 'status' attribute")
        logging.warning(f"Response content: {prediction}")
        return "Could not transcribe the audio"

    if status == "succeeded":
        output = prediction.get('output')
        if output and isinstance(output, dict) and "segments" in output:
            transcription = " ".join([segment["text"] for segment in output["segments"]])
            return transcription
        else:
            logging.warning("Output is missing or not in expected format")
            logging.warning(f"Output content: {output}")
            return "Could not transcribe the audio"
    elif status == "failed":
        error_message = prediction.get('error')
        if error_message:
            logging.error(f"Prediction failed with error: {error_message}")
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
