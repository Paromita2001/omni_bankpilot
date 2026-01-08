# services/tts.py

import pyttsx3
import uuid
import os
import threading

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

_engine_lock = threading.Lock()


def text_to_speech(text: str):
    """
    Offline TTS using pyttsx3 (thread-safe)
    """
    if not text or not text.strip():
        return None

    file_name = f"{uuid.uuid4().hex}.wav"
    file_path = os.path.join(AUDIO_DIR, file_name)

    with _engine_lock:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        # Try female voice if available
        voices = engine.getProperty("voices")
        for v in voices:
            if "female" in v.name.lower():
                engine.setProperty("voice", v.id)
                break

        engine.save_to_file(text, file_path)
        engine.runAndWait()
        engine.stop()

    return file_path
