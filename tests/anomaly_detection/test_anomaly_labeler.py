from app.services.anomaly_detection.anomaly_labeler import AnomalyLabeler


def test_not_anomalous():

    assert AnomalyLabeler.get_label(10.0) == "Nicht anomal"


def test_slightly_anomalous():

    assert AnomalyLabeler.get_label(30.0) == "Leicht anomal"


def test_anomalous():

    assert AnomalyLabeler.get_label(60.0) == "Anomal"


def test_highly_anomalous():

    assert AnomalyLabeler.get_label(90.0) == "Höchstanomal"
