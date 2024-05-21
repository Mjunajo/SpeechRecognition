from flask import Flask, request, render_template, redirect, url_for
import os
import logging
from speech_recognizer import recognize_speech_from_audio

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            file.save(file_path)
            text = recognize_speech_from_audio(file_path)
            return render_template('result.html', transcription=text)
        except Exception as e:
            app.logger.error(f"Error processing file: {e}")
            return "Internal Server Error", 500
