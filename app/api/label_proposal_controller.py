"""API router for label proposals.

Provides the endpoint the frontend uses to submit a category for a sample.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.label_proposal import LabelProposalCreate, LabelProposalResponse
from app.services.label_proposal_service import (
    LabelProposalError,
    LabelProposalService,
)

router = APIRouter(
    prefix="/sounds",
    tags=["labeling"],
)


@router.post("/labeled-samples", response_model=LabelProposalResponse)
def create_labeled_sample(
    proposal: LabelProposalCreate,
    session: Annotated[Session, Depends(get_session)],
) -> LabelProposalResponse:
    service = LabelProposalService(session)

    try:
        service.create_label_proposal(
            uuid=proposal.uuid,
            category_key=proposal.category,
        )
    except LabelProposalError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return LabelProposalResponse(
        message=f"Received label '{proposal.category}' for sample '{proposal.uuid}'.",
    )
