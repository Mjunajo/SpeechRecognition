from flask import Flask, request, render_template, redirect, url_for
import os
import replicate
from pydub import AudioSegment
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists in /tmp
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        text = recognize_speech_from_audio(file_path)
        return render_template('result.html', transcription=text)

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

    # Log the file path being processed
    logging.debug(f"Processing audio file: {audio_file_path}")

    # Define the model version explicitly
    version = client.models.get("openai/whisper").versions.get("4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2")

    # Upload audio file to Replicate
    with open(audio_file_path, 'rb') as f:
        model_input = {"audio": f}
        prediction = client.predictions.create(
            version=version,
            input=model_input
        )

    # Log the entire prediction object for debugging
    logging.debug(f"Prediction object: {prediction}")

    # Handle response
    if prediction.status == "succeeded" and prediction.output and "segments" in prediction.output:
        transcription = " ".join([segment["text"] for segment in prediction.output["segments"]])
        return transcription
    elif prediction.status == "failed" and prediction.error:
        logging.error(f"Prediction failed with error: {prediction.error}")
        return "Could not transcribe the audio"
    else:
        logging.warning("Unexpected response from Replicate API")
        logging.warning(f"Response content: {prediction}")
        return "Could not transcribe the audio"
