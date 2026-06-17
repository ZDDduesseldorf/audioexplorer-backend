import json
from pathlib import Path

from app.services.anomaly_detection.anomaly_service import (
    AnomalyService,
)

# LOCAL TEST:
# PYTHONPATH=. pytest tests/test_anomaly_pipeline.py -v

# This integration test verifies the complete anomaly detection pipeline.
#
# Test workflow:
# 1. Load embedding vectors from JSON files.
# 2. Build an embeddings dictionary using the file IDs as keys.
# 3. Execute the anomaly detection service.
# 4. Run both Isolation Forest and Local Outlier Factor detectors.
# 5. Generate anomaly scores and labels for each embedding.
# 6. Validate the structure and data types of the returned results.
# 7. Save the final results to a JSON file for inspection.
#
# Expected output:
# Each embedding should contain:
# - Isolation Forest score and label
# - Local Outlier Factor score and label
#
# You can find the output here:
# audioexplorer-backend/scripts/results
#


def test_full_anomaly_pipeline():

    embeddings_dir = Path("scripts/data/embeddings")

    embeddings = {}

    for file in sorted(embeddings_dir.glob("*.json")):
        with open(
            file,
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

            embeddings[data["id"]] = data["vector"]

    service = AnomalyService()

    results = service.calculate_anomalies(embeddings)

    assert len(results) > 0

    for embedding_id, result in results.items():
        assert "scores" in result

        assert "labels" in result

        assert "isolation_forest" in result["scores"]

        assert "lof" in result["scores"]

        assert "isolation_forest" in result["labels"]

        assert "lof" in result["labels"]

        assert isinstance(
            result["scores"]["isolation_forest"],
            float,
        )

        assert isinstance(
            result["scores"]["lof"],
            float,
        )

        assert isinstance(
            result["labels"]["isolation_forest"],
            str,
        )

        assert isinstance(
            result["labels"]["lof"],
            str,
        )

    output_dir = Path("scripts/results")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / "anomaly_results.json"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=4,
        )
