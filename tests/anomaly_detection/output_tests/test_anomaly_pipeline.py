import json

# TEST PRÜFT OB DIE PIPELINE FUNKTIONIERT 
# es erzeugt eine JSON-String im Speicher 
# TESTEN MIT

# PYTHONPATH=. pytest tests/anomaly_detection/output_tests/test_anomaly_pipeline.py -v


from app.services.anomaly_detection.embedding_loader import (
    EmbeddingLoader,
)

from app.services.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector,
)

from app.services.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector,
)


def test_embedding_scores():

    loader = EmbeddingLoader(
        "app/services/anomaly_detection/data/embeddings"
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

    target_index = 23

    output = {
        "embedding_id":
            f"embedding_{target_index + 1:03}",

        "scores": {

            "isolation_forest": {
                "anomaly_score":
                    round(
                        float(
                            isolation_results[
                                target_index
                            ]["normalized_score"]
                        ),
                        2,
                    )
            },

            "local_outlier_factor": {
                "anomaly_score":
                    round(
                        float(
                            lof_results[
                                target_index
                            ]["normalized_score"]
                        ),
                        2,
                    )
            },
        },
    }

    assert "embedding_id" in output

    assert "scores" in output

    assert (
        "isolation_forest"
        in output["scores"]
    )

    assert (
        "local_outlier_factor"
        in output["scores"]
    )

    json.dumps(output)