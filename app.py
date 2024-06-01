from flask import Flask, request, render_template, redirect, url_for
from speech_recognizer import SpeechRecognizer
import os

app = Flask(__name__)
recognizer = SpeechRecognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        text = recognizer.transcribe(file_path)
        os.remove(file_path)
        return render_template('result.html', transcription=text)

    return redirect(url_for('index'))


