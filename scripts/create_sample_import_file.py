from pathlib import Path

import numpy as np


def main() -> None:
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
                "crying",
            ],
            dtype="U100",
        ),
        category_keys=np.array(
            [
                "laugh",
                "cry",
            ],
            dtype="U100",
        ),
        filenames=np.array(
            [
                "a_RA1_01_01__xh6fC2ZfwU_moan.wav",
                "example_cry.wav",
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
    )

    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
