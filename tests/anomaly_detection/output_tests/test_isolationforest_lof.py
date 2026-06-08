

# PYTHONPATH=. pytest tests/anomaly_detection/output_tests/test_isolationforest_lof.py -v


import json
import os

from app.services.anomaly_detection.embedding_loader import (
    EmbeddingLoader,
)

from app.services.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector,
)

from app.services.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector,
)

EMBEDDING_DIR = (
    "app/services/anomaly_detection/data/embeddings"
)

OUTPUT_DIR = (
    "app/services/anomaly_detection/results"
)


def test_isolationforest_lof():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    loader = EmbeddingLoader(
        EMBEDDING_DIR
    )

    embeddings = loader.load_embeddings()

    assert len(embeddings) > 0

    isolation_detector = (
        IsolationForestDetector()
    )

    lof_detector = (
        LocalOutlierFactorDetector()
    )

    isolation_results = (
        isolation_detector.fit_predict(
            embeddings
        )
    )

    lof_results = (
        lof_detector.fit_predict(
            embeddings
        )
    )

    assert len(isolation_results) == len(
        embeddings
    )

    assert len(lof_results) == len(
        embeddings
    )

    for idx in range(
        len(embeddings)
    ):

        output = {

            "embedding_index": idx,

            "scores": {

                "isolation_forest": {

                    "anomaly_score":
                        float(
                            isolation_results[idx][
                                "normalized_score"
                            ]
                        )
                },

                "local_outlier_factor": {

                    "anomaly_score":
                        float(
                            lof_results[idx][
                                "normalized_score"
                            ]
                        )
                },
            },
        }

        output_file = os.path.join(
            OUTPUT_DIR,
            f"embedding_{idx:03}.json",
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                output,
                file,
                indent=4,
            )

    files = [
        file
        for file in os.listdir(
            OUTPUT_DIR
        )
        if file.endswith(".json")
    ]

    assert len(files) == len(
        embeddings
    )

    print(
        f"Created {len(files)} JSON files"
    )

