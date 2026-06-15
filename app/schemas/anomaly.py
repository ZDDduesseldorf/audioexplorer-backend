from pydantic import BaseModel


class Scores(BaseModel):
    isolation_forest: float
    lof: float


class Labels(BaseModel):
    isolation_forest: str
    lof: str


class AnomalyResponse(BaseModel):
    embedding_id: str
    scores: Scores
    labels: Labels
