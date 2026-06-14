import logging

import numpy as np
from sklearn.neighbors import LocalOutlierFactor  # type: ignore

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


class LocalOutlierFactorDetector(BaseDetector):
    def __init__(
        self,
        contamination=DetectorConfig.LOF["contamination"],
        n_neighbors=DetectorConfig.LOF["n_neighbors"],
        metric=DetectorConfig.LOF["metric"],
    ):

        self.model = LocalOutlierFactor(
            contamination=contamination,
            n_neighbors=n_neighbors,
            metric=metric,
        )

    def fit_predict(self, embeddings):

        validate_embeddings(embeddings)

        logger.info("Running LOF detection")

        embeddings_np = np.array(embeddings)

        # LOF ausführen

        raw_scores = self.model.negative_outlier_factor_

        normalized_scores = normalize_scores(-raw_scores)

        results = []

        for idx, score in enumerate(normalized_scores):
            results.append(
                {
                    "embedding_index": idx,
                    "algorithm": "Local Outlier Factor",
                    "raw_score": float(raw_scores[idx]),
                    "normalized_score": round(
                        float(score),
                        2,
                    ),
                }
            )

        return results
