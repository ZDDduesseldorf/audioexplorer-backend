# Loads an audio file and resamples it to the CLAP sample rate.

from pathlib import Path
import librosa
import numpy as np
from app.services.model_manager import CLAP_SAMPLE_RATE

def load_audio(file_path: Path) -> np.ndarray:
    waveform, _ = librosa.load(str(file_path), sr=CLAP_SAMPLE_RATE, mono=True)
    return waveform.astype(np.float32)
