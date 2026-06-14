from app.services.anomaly_detection.anomaly_service import AnomalyService

# PYTHONPATH=. pytest tests/anomaly_detection/output_tests/test_api_antwort.py -v

def test_service_returns_expected_response_structure():
    service = AnomalyService()

    result = service.get_scores(0)

    assert "embedding_id" in result
    assert "scores" in result
    assert "labels" in result

    assert "isolation_forest" in result["scores"]
    assert "lof" in result["scores"]

    assert isinstance(
        result["scores"]["isolation_forest"],
        float,
    )
    assert isinstance(
        result["scores"]["lof"],
        float,
    )

    assert "isolation_forest" in result["labels"]
    assert "lof" in result["labels"]

    assert isinstance(
        result["labels"]["isolation_forest"],
        str,
    )
    assert isinstance(
        result["labels"]["lof"],
        str,
    )

    assert result["embedding_id"].startswith(
        "embedding_",
    )