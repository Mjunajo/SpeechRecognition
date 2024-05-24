import os
import replicate
from pydub import AudioSegment
from pydub.utils import which
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set path to the local ffmpeg and ffprobe binaries
ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg')
ffprobe_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffprobe')

# Set pydub to use these binaries
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

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

    # Poll the API to get the result
    while prediction.status not in ["succeeded", "failed"]:
        prediction.reload()
    
    # Log the output for debugging
    logging.debug(f"Replicate API output: {prediction}")

    if prediction.status == "succeeded" and prediction.output and "segments" in prediction.output:
        transcription = " ".join([segment["text"] for segment in prediction.output["segments"]])
        return transcription
    else:
        return "Could not transcribe the audio"
