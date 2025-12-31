import speech_recognition as sr
import tempfile
import soundfile as sf
import numpy as np
import os

recognizer = sr.Recognizer()

def speech_to_text(audio):
    """
    Converts Gradio audio input to text
    """

    if audio is None:
        return ""

    if not isinstance(audio, (tuple, list)) or len(audio) != 2:
        return ""

    audio_array, sample_rate = audio

    if not isinstance(audio_array, np.ndarray):
        return ""

    # Ensure mono audio (important)
    if audio_array.ndim == 2:
        audio_array = np.mean(audio_array, axis=1)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        temp_filename = f.name

    try:
        sf.write(temp_filename, audio_array, sample_rate)

        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language="en-IN"
        )

        return text.strip()

    except sr.UnknownValueError:
        print("STT: Could not understand audio")
        return ""

    except sr.RequestError as e:
        print("STT API Error:", e)
        return ""

    except Exception as e:
        print("STT Error:", e)
        return ""

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
