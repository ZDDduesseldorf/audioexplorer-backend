import pandas as pd
from pathlib import Path


def load_metadata_as_df(path: Path):
    metadata = pd.read_csv(path, sep=";")

    return metadata


def build_audio_path_from_metadata(uuid: str):
    BASE_DIR = Path(__file__).resolve().parents[2]
    metadata_path = BASE_DIR / "data" / "metadata.csv"
    df = load_metadata_as_df(metadata_path)
    row = df[df["uuid"] == uuid]
    filename = row.filename.item()
    source = row.source.item()

    audio_path = "data/" + source + "/" + filename
    return audio_path


def load_all_metadata():
    BASE_DIR = Path(__file__).resolve().parents[2]
    metadata_path = BASE_DIR / "data" / "metadata.csv"
    df = load_metadata_as_df(metadata_path)

    metadata = {}

    for _, row in df.iterrows():
        metadata[row.uuid] = {
            "label": row.label,
            "category": row.category,
            "filename": row.filename,
        }

    return metadata
