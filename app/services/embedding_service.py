# Computes audio embeddings from raw waveforms using a loaded ModelManager.

import numpy as np
import torch

from app.services.model_manager import CLAP_SAMPLE_RATE, ModelManager


def compute_embedding(waveform: np.ndarray, manager: ModelManager) -> np.ndarray:
    inputs = manager.processor(
        audios=waveform,
        return_tensors="pt",
        sampling_rate=CLAP_SAMPLE_RATE,
    )
    with torch.no_grad():
        features = manager.model.get_audio_features(**inputs)
    result: np.ndarray = features.cpu().numpy()
    return result  # shape: (1, 512)


def compute_embeddings_batch(
    waveforms: list[np.ndarray], manager: ModelManager
) -> np.ndarray:
    embeddings = [compute_embedding(w, manager) for w in waveforms]
    return np.vstack(embeddings)  # shape: (N, 512)
