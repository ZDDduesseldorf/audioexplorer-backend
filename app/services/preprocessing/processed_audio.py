from dataclasses import dataclass

import numpy as np


@dataclass
class ProcessedAudio:
    uuid: str
    audio: np.ndarray
