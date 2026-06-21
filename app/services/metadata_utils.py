import pandas as pd
from pathlib import Path


def load_metadata_as_df(path: Path):
    metadata = pd.read_json(path)

    return metadata


def load_all_metadata(path_metadata):
    df = load_metadata_as_df(path_metadata)

    metadata = {}

    for _, row in df.iterrows():
        metadata[row.uuid] = {
            "label": row.label,
            "category": row.category,
            "filename": row.filename,
        }

    return metadata
