from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DATA_DIR = PROJECT_ROOT / "data"


DEFAULT_TESTDATA_DIR = PROJECT_ROOT / "testdata"

DATA_DIR = (
    Path(os.getenv("AUDIO_EXPLORER_DATA_DIR", DEFAULT_DATA_DIR)).expanduser().resolve()
)


TESTDATA_DIR = (
    Path(os.getenv("AUDIO_EXPLORER_DATA_DIR", DEFAULT_TESTDATA_DIR))
    .expanduser()
    .resolve()
)


def get_data_file_path(filename: str) -> Path:
    return DATA_DIR / filename


def get_data_dir() -> Path:
    return DATA_DIR


def get_testdata_dir() -> Path:
    return TESTDATA_DIR
