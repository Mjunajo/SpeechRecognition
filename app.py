from flask import Flask, render_template, request, redirect, url_for
import os
import tempfile
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
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        file.save(tmp_file.name)
        tmp_file_path = tmp_file.name

    # Convert audio to text using the speech recognizer
    result = convert_audio_to_text(tmp_file_path)
    
    # Clean up the temporary file
    os.remove(tmp_file_path)

    return render_template('result.html', text=result)

