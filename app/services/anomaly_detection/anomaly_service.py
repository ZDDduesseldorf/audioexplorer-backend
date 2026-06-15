from app.services.anomaly_detection.embedding_loader import (
    EmbeddingLoader,
)

from app.services.anomaly_detection.detectors.isolation_forest_detector import (
    IsolationForestDetector,
)

from app.services.anomaly_detection.detectors.lof_detector import (
    LocalOutlierFactorDetector,
)

from app.services.anomaly_detection.anomaly_labeler import (
    AnomalyLabeler,
)


class AnomalyService:

    def get_scores(
        self,
        embedding_index: int,
    ) -> dict:

        all_results = self.calculate_anomalies()

        embedding_id = (
            f"embedding_{embedding_index + 1:03}"
        )

        return {
            "embedding_id": embedding_id,
            "scores": all_results[
                embedding_id
            ]["scores"],
            "labels": all_results[
                embedding_id
            ]["labels"],
        }

    def calculate_anomalies(
        self,
    ) -> dict:

        loader = EmbeddingLoader(
            "app/services/anomaly_detection/data/embeddings"
        )

        embedding_vectors = (
            loader.load_embeddings()
        )

        embedding_ids = [
            f"embedding_{index + 1:03}"
            for index in range(
                len(embedding_vectors)
            )
        ]

        isolation_detector = (
            IsolationForestDetector()
        )

        lof_detector = (
            LocalOutlierFactorDetector()
        )

        isolation_results = (
            isolation_detector.fit_predict(
                embedding_vectors
            )
        )

        lof_results = (
            lof_detector.fit_predict(
                embedding_vectors
            )
        )

        results = {}

        for index, embedding_id in enumerate(
            embedding_ids
        ):

            isolation_score = (
                isolation_results[index]
                ["normalized_score"]
            )

            lof_score = (
                lof_results[index]
                ["normalized_score"]
            )

            results[embedding_id] = {

                "scores": {

                    "isolation_forest":
                        round(
                            isolation_score,
                            2,
                        ),

                    "lof":
                        round(
                            lof_score,
                            2,
                        ),
                },

                "labels": {

                    "isolation_forest":
                        AnomalyLabeler.get_label(
                            isolation_score
                        ),

                    "lof":
                        AnomalyLabeler.get_label(
                            lof_score
                        ),
                },
            }

        return results