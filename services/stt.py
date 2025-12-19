# services/stt.py
import speech_recognition as sr
import tempfile
import soundfile as sf
import numpy as np
import os

def speech_to_text(audio):
    """
    Handles Gradio 6.1.0 audio formats safely
    """

    # Case 1: no audio / invalid trigger
    if audio is None:
        return ""

    # Case 2: audio is not (array, sample_rate)
    if not isinstance(audio, (tuple, list)) or len(audio) != 2:
        return ""

    audio_array, sample_rate = audio

    # Case 3: audio_array is not numpy array
    if not isinstance(audio_array, np.ndarray):
        return ""

    # Ensure 2D (samples, channels)
    if audio_array.ndim == 1:
        audio_array = audio_array.reshape(-1, 1)

    # Save temporary wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        temp_filename = f.name

    sf.write(temp_filename, audio_array, sample_rate)

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_filename) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except Exception:
        text = ""
    finally:
        os.remove(temp_filename)

    return text
