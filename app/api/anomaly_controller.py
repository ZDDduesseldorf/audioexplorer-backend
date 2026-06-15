from fastapi import APIRouter

from app.schemas.anomaly import (
    AnomalyResponse,
)

from app.services.anomaly_detection.anomaly_service import (
    AnomalyService,
)

router = APIRouter(
    prefix="/anomaly",
    tags=["anomaly"],
)

service = AnomalyService()


@router.get(
    "/analyze",
)
def analyze_all_embeddings():

    return service.calculate_anomalies()


@router.get(
    "/{embedding_index}",
    response_model=AnomalyResponse,
)
def get_anomaly_score(
    embedding_index: int,
):

    return service.get_scores(embedding_index)
