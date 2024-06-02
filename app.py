# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
from speech_recognizer import convert_audio_to_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # Save file temporarily
    file_path = os.path.join("static", file.filename)
    file.save(file_path)

    # Convert audio to text using the speech recognizer
    result = convert_audio_to_text(file_path)
    os.remove(file_path)  # Remove the temporary file after processing

    return render_template('result.html', text=result)
