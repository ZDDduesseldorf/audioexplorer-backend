from app.services.anomaly_detection.anomaly_service import (
    AnomalyService,
)

# python -m pytest tests/anomaly_detection/test_calculate_anomalies.py -v
# DER TEST PRÜFT, OB
# calculate_anomalies DIE RICHTIGE SCHNITTSTELLE UND STRUKTUR LIEFERT.

# DER TEST KONTROLLIERT GENAU:
# Ist das Ergebnis ein Dictionary?
# Sind die UUIDS vorhanden?
# Gibt es den Bereich Scores?
# Gibt es den Bereich Labels?
# Sind die beide ALgorithmen vorhanden?
# Sind die Scores Zahlen?
# Sind die Labels Strings?


def test_calculate_anomalies_returns_expected_structure():

    embeddings = {
        "uuid1": [0.1, 0.2, 0.3, 0.4],
        "uuid2": [1.1, 1.2, 1.3, 1.4],
        "uuid3": [2.1, 2.2, 2.3, 2.4],
    }

    service = AnomalyService()

    result = service.calculate_anomalies(embeddings)

    # IST DAS ERGEBNIS EIN DICTIONARY?
    assert isinstance(result, dict)

    # Sind die UUIDS vorhanden?
    # [
    # ...
    # ]
    assert "uuid1" in result
    assert "uuid2" in result
    assert "uuid3" in result

    # Gibt es den Bereich Scores?
    assert "scores" in result["uuid1"]

    # Gibt es den Bereich Labels?
    assert "labels" in result["uuid1"]

    # Sind beide Algorithmen vorhanden?
    assert "isolation_forest" in result["uuid1"]["scores"]
    assert "lof" in result["uuid1"]["scores"]

    assert "isolation_forest" in result["uuid1"]["labels"]
    assert "lof" in result["uuid1"]["labels"]

    # Sind die Scores Zahlen?
    assert isinstance(
        result["uuid1"]["scores"]["isolation_forest"],
        float,
    )

    assert isinstance(
        result["uuid1"]["scores"]["lof"],
        float,
    )

    # Sind die Labels Strings?
    assert isinstance(
        result["uuid1"]["labels"]["isolation_forest"],
        str,
    )

    assert isinstance(
        result["uuid1"]["labels"]["lof"],
        str,
    )
