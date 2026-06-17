from app.services.anomaly_detection.anomaly_service import (
    AnomalyService,
)

# LOCAL TEST:
# PYTHONPATH=. pytest tests/test_calculate_anomalies_function.py -v
#
# Unit test for the calculate_anomalies() method.
#
# This test verifies that the anomaly detection service can process
# a dictionary of embedding vectors and return results in the expected format.
#
# Test workflow:
# 1. Create a small set of sample embeddings.
# 2. Execute the anomaly detection service.
# 3. Verify that a dictionary is returned.
# 4. Verify that all input IDs exist in the output.
# 5. Verify that scores and labels are generated.
# 6. Verify that score values are floats.
# 7. Verify that label values are strings.
# 8. Verify that normalized scores are within the range 0-100.
#
# Expected output:
# Each embedding should contain:
# - Isolation Forest score
# - Local Outlier Factor score
# - Isolation Forest label
# - Local Outlier Factor label
#


def test_calculate_anomalies_accepts_embedding_dictionary():
    # Create a dictionary exactly like the one
    # that will later be produced by the embedding pipeline

    embeddings = {
        "audio_001": [0.1, 0.2, 0.3, 0.4],
        "audio_002": [1.1, 1.2, 1.3, 1.4],
        "audio_003": [2.1, 2.2, 2.3, 2.4],
    }

    # Create the anomaly service

    service = AnomalyService()

    # Run anomaly detection on all embeddings

    results = service.calculate_anomalies(embeddings)

    # Verify that a dictionary is returned

    assert isinstance(
        results,
        dict,
    )

    # Verify that all input IDs are present
    # in the output

    assert "audio_001" in results
    assert "audio_002" in results
    assert "audio_003" in results

    # Verify output structure for one audio sample

    sample = results["audio_001"]

    assert "scores" in sample
    assert "labels" in sample

    # Verify score fields

    assert "isolation_forest" in sample["scores"]

    assert "lof" in sample["scores"]

    # Verify label fields

    assert "isolation_forest" in sample["labels"]

    assert "lof" in sample["labels"]

    # Verify score data types

    assert isinstance(
        sample["scores"]["isolation_forest"],
        float,
    )

    assert isinstance(
        sample["scores"]["lof"],
        float,
    )

    # Verify label data types

    assert isinstance(
        sample["labels"]["isolation_forest"],
        str,
    )

    assert isinstance(
        sample["labels"]["lof"],
        str,
    )

    # Verify score range after normalization

    assert 0 <= sample["scores"]["isolation_forest"] <= 100

    assert 0 <= sample["scores"]["lof"] <= 100
