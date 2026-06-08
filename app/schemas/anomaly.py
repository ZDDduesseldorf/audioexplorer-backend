from pydantic import BaseModel


class DetectorScore(BaseModel):
    anomaly_score: float


class AnomalyScores(BaseModel):
    isolation_forest: DetectorScore
    local_outlier_factor: DetectorScore


class AnomalyResponse(BaseModel):
    embedding_id: str
    scores: AnomalyScores