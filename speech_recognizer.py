import whisper
import os
import subprocess

class SpeechRecognizer:
    def __init__(self, model_name='base'):
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path):
        # Convert mp3 to wav if needed
        if audio_path.endswith('.mp3'):
            wav_path = audio_path.replace('.mp3', '.wav')
            self.convert_mp3_to_wav(audio_path, wav_path)
            audio_path = wav_path
        
        result = self.model.transcribe(audio_path)
        return result['text']
    
    def convert_mp3_to_wav(self, mp3_path, wav_path):
        subprocess.run(['ffmpeg', '-i', mp3_path, wav_path], check=True)
