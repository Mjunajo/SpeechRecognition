from flask import Flask, request, render_template, redirect, url_for
import os
from speech_recognizer import recognize_speech_from_audio
import tempfile

app = Flask(__name__)

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
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            text = recognize_speech_from_audio(temp_file.name)
        return render_template('result.html', transcription=text)
