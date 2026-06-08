from app.services.anomaly_detection.embedding_loader import (
    EmbeddingLoader
)

from app.services.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector
)

from app.services.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector
)


class AnomalyService:

    def get_scores(
        self,
        embedding_index: int
    ):

        loader = EmbeddingLoader(
            "data/embeddings"
        )

        embeddings = loader.load_embeddings()

        isolation = (
            IsolationForestDetector()
        )

        lof = (
            LocalOutlierFactorDetector()
        )

        isolation_results = (
            isolation.fit_predict(
                embeddings
            )
        )

        lof_results = (
            lof.fit_predict(
                embeddings
            )
        )

        return {
            "embedding_id":
                f"embedding_{embedding_index + 1:03}",

            "scores": {

                "isolation_forest": {
                    "anomaly_score":
                        isolation_results[
                            embedding_index
                        ]["normalized_score"]
                },

                "local_outlier_factor": {
                    "anomaly_score":
                        lof_results[
                            embedding_index
                        ]["normalized_score"]
                }
            }
        }