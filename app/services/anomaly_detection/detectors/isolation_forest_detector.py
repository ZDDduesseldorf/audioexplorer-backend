import logging

import numpy as np
from sklearn.ensemble import IsolationForest

from app.services.anomaly_detection.detectors.base_detector import (
    BaseDetector,
)

from app.services.anomaly_detection.utils.detector_config import (
    DetectorConfig,
)

from app.services.anomaly_detection.utils.normalization import (
    normalize_scores,
)

from app.services.anomaly_detection.utils.validation import (
    validate_embeddings,
)

logger = logging.getLogger(__name__)


class IsolationForestDetector(BaseDetector):

    def __init__(
        self,
        contamination=DetectorConfig.ISOLATION_FOREST["contamination"],
        n_estimators=DetectorConfig.ISOLATION_FOREST["n_estimators"],
        random_state=DetectorConfig.ISOLATION_FOREST["random_state"],
    ):

        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
        )

    def fit_predict(self, embeddings):

        validate_embeddings(embeddings)

        logger.info(
            "Running Isolation Forest detection"
        )

        embeddings_np = np.array(
            embeddings
        )

        raw_predictions = (
            self.model.fit_predict(
                embeddings_np
            )
        )

        decision_scores = (
            self.model.decision_function(
                embeddings_np
            )
        )

        normalized_scores = (
            normalize_scores(
                -decision_scores
            )
        )

        results = []

        for idx, score in enumerate(
            normalized_scores
        ):

            results.append(
                {
                    "embedding_index": idx,
                    "algorithm":
                        "Isolation Forest",
                    "raw_score":
                        float(
                            decision_scores[idx]
                        ),
                    "normalized_score":
                        round(
                            float(score),
                            2
                        ),
                }
            )

        return results