import speech_recognition as sr

def recognize_speech_from_audio(audio_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
    
    # Recognize (convert from speech to text)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Example usage (for testing)
if __name__ == "__main__":
    audio_path = "path_to_your_audio_file.wav"  # Replace with your audio file path
    print(recognize_speech_from_audio(audio_path))
