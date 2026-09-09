import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8")

SAMPLE_RATE = 16000
DURATION = 5  # seconds


def record_audio():
    print("🎤 Listening...")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()


def speech_to_text():
    audio = record_audio()
    segments, _ = model.transcribe(audio, language="en")

    text = ""
    for segment in segments:
        text += segment.text

    return text.strip()
