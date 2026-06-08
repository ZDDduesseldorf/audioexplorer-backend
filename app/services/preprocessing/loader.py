from pathlib import Path

import librosa
import numpy as np


class LocalAudioLoader:
    def load(self, file_path: Path) -> tuple[np.ndarray, int]:
        audio, sample_rate = librosa.load(
            file_path,
            sr=None,
            mono=True,
        )

        return audio, sample_rate


# TODO: DatabaseAudioLoader
