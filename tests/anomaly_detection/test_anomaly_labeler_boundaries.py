from app.services.anomaly_detection.anomaly_labeler import AnomalyLabeler


def test_boundary_19():

    assert AnomalyLabeler.get_label(19.0) == "Nicht anomal"


def test_boundary_20():

    assert AnomalyLabeler.get_label(20.0) == "Leicht anomal"


def test_boundary_50():

    assert AnomalyLabeler.get_label(50.0) == "Anomal"


def test_boundary_80():

    assert AnomalyLabeler.get_label(80.0) == "Höchstanomal"
