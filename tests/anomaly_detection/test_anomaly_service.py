from app.services.anomaly_detection.anomaly_service import AnomalyService


def test_service_returns_expected_fields():

    service = AnomalyService()

    result = service.get_scores(0)

    assert "embedding_id" in result
    assert "scores" in result
    assert "labels" in result

    assert "isolation_forest" in result["scores"]
    assert "lof" in result["scores"]

    assert "isolation_forest" in result["labels"]
    assert "lof" in result["labels"]
