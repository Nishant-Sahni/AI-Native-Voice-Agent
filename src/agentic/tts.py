import time
import numpy as np
import sounddevice as sd
from TTS.api import TTS
import threading

speech_lock = threading.Lock()
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

BASE_SR = 22050  # Tacotron2 output sample rate


def normalize_text(text: str) -> str:
    return (
        text.replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("–", "-")
            .replace("…", "...")
    )


def speak(text: str, speed: float = 0.85):
    with speech_lock:
        """
        speed < 1.0  -> slower, calmer
        speed = 1.0  -> normal
        """

        text = normalize_text(text)

        time.sleep(0.4)  # human-like thinking pause

        wav = tts.tts(text)

        # 🔑 CRITICAL FIX: ensure numpy array
        wav = np.asarray(wav, dtype=np.float32)

        # soften volume slightly
        wav *= 0.9

        # slow speech by lowering playback rate
        #playback_sr = int(BASE_SR * speed)

        sd.play(wav, samplerate=22050)
        sd.wait()
