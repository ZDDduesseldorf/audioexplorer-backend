from pathlib import Path
from unittest.mock import patch

import numpy as np

from app.services.audio_loader import load_audio
from app.services.model_manager import CLAP_SAMPLE_RATE


@patch("app.services.audio_loader.librosa.load")
def test_output_is_float32(mock_load: object) -> None:
    mock_load.return_value = (  # type: ignore[attr-defined]
        np.zeros(CLAP_SAMPLE_RATE, dtype=np.float64),
        CLAP_SAMPLE_RATE,
    )

    result = load_audio(Path("test.wav"))

    assert result.dtype == np.float32


@patch("app.services.audio_loader.librosa.load")
def test_librosa_is_called_with_correct_sample_rate_and_mono(mock_load: object) -> None:
    mock_load.return_value = (np.zeros(100, dtype=np.float32), CLAP_SAMPLE_RATE)  # type: ignore[attr-defined]

    load_audio(Path("audio.wav"))

    mock_load.assert_called_once_with(  # type: ignore[attr-defined]
        str(Path("audio.wav")), sr=CLAP_SAMPLE_RATE, mono=True
    )


@patch("app.services.audio_loader.librosa.load")
def test_waveform_length_is_unchanged(mock_load: object) -> None:
    expected = np.ones(CLAP_SAMPLE_RATE, dtype=np.float32)
    mock_load.return_value = (expected, CLAP_SAMPLE_RATE)  # type: ignore[attr-defined]

    result = load_audio(Path("audio.wav"))

    assert result.shape == (CLAP_SAMPLE_RATE,)
