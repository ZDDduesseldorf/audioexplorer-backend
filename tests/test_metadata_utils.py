import app.services.metadata_utils as meta
import pandas as pd


def test_load_metadata_as_df(tmp_path):
    file = tmp_path / "meta.csv"

    df = pd.DataFrame(
        {
            "uuid": ["1"],
            "filename": ["a.wav"],
            "label": ["laugh"],
            "category": ["x"],
            "source": ["folder1"],
        }
    )

    df.to_csv(file, sep=";", index=False)

    result = meta.load_metadata_as_df(file)

    assert len(result) == 1
    assert "uuid" in result.columns
