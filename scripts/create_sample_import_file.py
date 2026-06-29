from pathlib import Path

import numpy as np


def create_sample_category_import_file() -> None:
    output_path = Path("sample_category_import.npz")

    np.savez_compressed(
        output_path,
        ids=np.array(
            [
                100,
                101,
            ],
            dtype=np.int64,
        ),
        category_keys=np.array(
            [
                "music",
                "dog",
            ],
            dtype="U100",
        ),
        display_names=np.array(
            [
                "Musik",
                "Hund",
            ],
            dtype="U100",
        ),
    )

    print(f"Created {output_path}")


def create_sample_data_overview_import_file() -> None:
    output_path = Path("sample_data_overview_import.npz")

    np.savez_compressed(
        output_path,
        uuids=np.array(
            [
                "4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a",
                "5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
            ],
            dtype="U36",
        ),
        umap=np.array(
            [
                [1.1, 2.2, 0.0],
                [3.3, 4.4, 0.0],
            ],
            dtype=np.float64,
        ),
        labels=np.array(
            [
                "laughing",
                "barking",
            ],
            dtype="U100",
        ),
        category_keys=np.array(
            [
                "music",
                "dog",
            ],
            dtype="U100",
        ),
        filenames=np.array(
            [
                "sample_music.wav",
                "sample_dog.wav",
            ],
            dtype="U255",
        ),
        anomalie_isolation_forest=np.array(
            [
                58.6,
                12.3,
            ],
            dtype=np.float64,
        ),
        anomalie_lof=np.array(
            [
                59.7,
                13.4,
            ],
            dtype=np.float64,
        ),
        anomalie_lof_labels=np.array(
            [
                "noise",
                "normal",
            ],
            dtype="U100",
        ),
        anomalie_isolation_forest_labels=np.array(
            [
                "noise",
                "normal",
            ],
            dtype="U100",
        ),
        nearest_neighbors=np.array(
            [
                '{"5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b": 0.12}',
                '{"4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a": 0.12}',
            ],
            dtype="U1000",
        ),
    )

    print(f"Created {output_path}")


def main() -> None:
    create_sample_category_import_file()
    create_sample_data_overview_import_file()


if __name__ == "__main__":
    main()
