import pytest

from app.services.anomaly_detection.anomaly_service import (
    AnomalyService,
)


def test_calculate_anomalies_raises_for_non_numeric_values():
    """
    Verify that anomaly calculation rejects non-numeric values.

    Goal:
        Ensure embeddings contain only numeric values.

    Covered code:
        validation.py
        if not isinstance(value, (int, float)):
            raise TypeError(...)

    Why this test matters:
        Machine learning algorithms require numerical
        vectors. Invalid values must be detected before
        model execution.
    """

    service = AnomalyService()

    embeddings = {
        "audio_001": [1.0, "invalid", 3.0],
    }

    with pytest.raises(TypeError):
        service.calculate_anomalies(embeddings)


def test_calculate_anomalies_raises_for_empty_embedding():

    service = AnomalyService()

    embeddings = {
        "audio_001": [],
    }

    with pytest.raises(ValueError):
        service.calculate_anomalies(embeddings)


def test_calculate_anomalies_raises_for_string_inside_embedding():

    service = AnomalyService()

    embeddings = {
        "audio_001": [1.0, "abc", 3.0],
    }

    with pytest.raises(TypeError):
        service.calculate_anomalies(embeddings)


def test_calculate_anomalies_raises_for_non_list_embedding():

    service = AnomalyService()

    embeddings = {
        "audio_001": "invalid",
    }

    with pytest.raises(TypeError):
        service.calculate_anomalies(embeddings)
