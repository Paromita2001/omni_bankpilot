# services/stt.py

import whisper
import os
import tempfile
import subprocess
import uuid

# Load smallest CPU-safe Whisper model
model = whisper.load_model("tiny")


def convert_to_wav(input_path: str) -> str:
    """
    Convert any audio file to 16kHz mono WAV (Whisper safe)
    """
    temp_dir = tempfile.gettempdir()
    out_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        out_path
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if not os.path.exists(out_path):
        raise RuntimeError("Audio conversion failed")

    return out_path


def speech_to_text(audio_path: str) -> str:
    if not audio_path or not os.path.exists(audio_path):
        print("❌ Audio path not found:", audio_path)
        return ""

    try:
        print("🎙️ STT input file:", audio_path)
        safe_wav = convert_to_wav(audio_path)
        print("🎧 Converted wav:", safe_wav)

        result = model.transcribe(
            safe_wav,
            language="en",
            fp16=False,
            temperature=0.0
        )

        print("🧠 Whisper raw output:", result)

        text = result.get("text", "").strip()
        print("📝 Final text:", text)
        return text

    except Exception as e:
        print("🔴 STT Error:", e)
        return ""


    finally:
        # Cleanup temp wav
        try:
            if 'safe_wav' in locals() and os.path.exists(safe_wav):
                os.remove(safe_wav)
        except:
            pass
