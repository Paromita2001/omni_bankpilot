import pyttsx3
import tempfile
import os

def text_to_speech(text):
    if not text:
        return None

    engine = pyttsx3.init()   # ✅ init per call (safe)
    engine.setProperty("rate", 170)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        audio_path = f.name

    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    engine.stop()

    return audio_path
