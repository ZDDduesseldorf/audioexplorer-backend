class AnomalyLabeler:
    NOT_ANOMALOUS = "Nicht anomal"
    SLIGHTLY_ANOMALOUS = "Leicht anomal"
    ANOMALOUS = "Anomal"
    HIGHLY_ANOMALOUS = "Höchstanomal"

    @staticmethod
    def get_label(score: float) -> str:

        if score < 0 or score > 100:
            raise ValueError("Anomaly score must be between 0 and 100")

        if score <= 19.99:
            return AnomalyLabeler.NOT_ANOMALOUS

        if score <= 49.99:
            return AnomalyLabeler.SLIGHTLY_ANOMALOUS

        if score <= 79.99:
            return AnomalyLabeler.ANOMALOUS

        return AnomalyLabeler.HIGHLY_ANOMALOUS

    @staticmethod
    def create_labels(isolation_score: float, lof_score: float) -> dict:

        return {
            "isolation_forest_label": AnomalyLabeler.get_label(isolation_score),
            "local_outlier_factor_label": AnomalyLabeler.get_label(lof_score),
        }
