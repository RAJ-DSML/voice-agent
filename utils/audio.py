import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

SAMPLE_RATE = 16000  # Whisper expects 16kHz
CHANNELS = 1         # Mono


def record_audio(duration: int = 8) -> str:
    """
    Records audio from the default microphone for a given duration.
    Saves it as a temp WAV file and returns the file path.
    """
    print(f"[audio] Recording for {duration} seconds...")

    audio_data = sd.rec(
        frames=int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
    )
    sd.wait()  # Block until recording is complete

    print("[audio] Recording complete.")

    # Write to a temp WAV file
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav.write(tmp.name, SAMPLE_RATE, audio_data)

    return tmp.name


def cleanup_audio(file_path: str) -> None:
    """
    Deletes the temp WAV file after it's been processed.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[audio] Cleaned up {file_path}")