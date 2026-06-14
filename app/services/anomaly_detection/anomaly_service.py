from app.services.anomaly_detection.embedding_loader import EmbeddingLoader

from app.services.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector,
)

from app.services.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector,
)

from app.services.anomaly_detection.anomaly_labeler import AnomalyLabeler


class AnomalyService:
    def get_scores(self, embedding_index: int):

        loader = EmbeddingLoader("app/services/anomaly_detection/data/embeddings")

        embeddings = loader.load_embeddings()

        isolation_detector = IsolationForestDetector()

        lof_detector = LocalOutlierFactorDetector()

        isolation_results = isolation_detector.fit_predict(embeddings)

        lof_results = lof_detector.fit_predict(embeddings)

        isolation_score = isolation_results[embedding_index]["normalized_score"]

        lof_score = lof_results[embedding_index]["normalized_score"]

        isolation_label = AnomalyLabeler.get_label(isolation_score)

        lof_label = AnomalyLabeler.get_label(lof_score)

        return {
            "embedding_id": f"embedding_{embedding_index + 1:03}",
            "scores": {
                "isolation_forest": round(isolation_score, 2),
                "lof": round(lof_score, 2),
            },
            "labels": {"isolation_forest": isolation_label, "lof": lof_label},
        }
