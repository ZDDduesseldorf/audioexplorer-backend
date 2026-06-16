from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR = (
    Path(os.getenv("AUDIO_EXPLORER_DATA_DIR", DEFAULT_DATA_DIR)).expanduser().resolve()
)


def get_data_file_path(filename: str) -> Path:
    return DATA_DIR / filename
