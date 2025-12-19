# services/tts.py
import pyttsx3
import tempfile
import os

engine = pyttsx3.init()

def text_to_speech(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        filename = f.name

    engine.save_to_file(text, filename)
    engine.runAndWait()

    return filename
