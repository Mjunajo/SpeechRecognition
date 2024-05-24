from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import logging
from speech_recognizer import recognize_speech_from_audio

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
DOWNLOAD_FOLDER = '/tmp/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        app.logger.error('No selected file')
        return redirect(request.url)

    if file:
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)

            # Recognize speech and save the transcription to a text file
            text = recognize_speech_from_audio(file_path)
            transcription_file = f"{os.path.splitext(file.filename)[0]}.txt"
            transcription_path = os.path.join(app.config['DOWNLOAD_FOLDER'], transcription_file)
            os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
            with open(transcription_path, 'w') as f:
                f.write(text)

            return render_template('result.html', transcription=text, transcription_file=transcription_file)
        except Exception as e:
            app.logger.error(f"Error processing file: {e}")
            return "Internal Server Error", 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)
