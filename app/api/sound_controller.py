"""API router for sound-related endpoints.

Provides endpoints to list data overviews, retrieve a single overview by UUID,
stream audio files by UUID, list categories, retrieve a category by ID, and
serve example labeled samples. Each endpoint returns Pydantic models defined
in app.schemas.sound and uses services from app.services to load data.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from typing import Annotated
from app.db.session import get_session

from app.schemas.sound import CategoryListItem, DataOverviewResponse
from app.services.data_overview_service import load_all_data_overview, load_data_by_uuid
from app.services.category_service import (
    load_all_categories,
    load_category_by_id,
    load_category_by_key,
)
from app.services.audio_utils import find_audio_url_by_uuid

router = APIRouter(
    prefix="/sounds",
    tags=["sounds"],
)


@router.get("/overviews", response_model=list[DataOverviewResponse])
def get_all_data_overviews(
    session: Annotated[Session, Depends(get_session)],
) -> list[DataOverviewResponse]:
    """Return a list of all DataOverview objects.

    Uses the data overview service to load and return all available
    DataOverview entries.
    """

    all_data = load_all_data_overview(session)

    return all_data


@router.get("/overviews/{uuid}", response_model=DataOverviewResponse)
def get_data_overview_by_uuid(
    uuid: str,
    session: Annotated[Session, Depends(get_session)],
) -> DataOverviewResponse:
    """Return a single DataOverview object by UUID."""
    data_uuid = load_data_by_uuid(uuid, session)
    return data_uuid


# TODO: Endpunkt der AudioURL übergibt, um die Audiodatei abzuspielen
@router.get("/audio/{uuid}")
def get_audio_by_uuid(uuid: str):
    """Return a FileResponse for the audio file corresponding to the given UUID."""

    audio_path = find_audio_url_by_uuid(uuid)
    return FileResponse(
        path=audio_path, media_type="audio/wav", filename=audio_path.name
    )


@router.get("/categories", response_model=list[CategoryListItem])
def get_category_list(
    session: Annotated[Session, Depends(get_session)],
) -> list[CategoryListItem]:
    """Return a list of all CategoryListItem objects."""

    catergory_list = load_all_categories(session)
    return catergory_list


@router.get("/categories/id/{category_id}", response_model=CategoryListItem)
def get_category_by_id(
    category_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> CategoryListItem:
    """Return a single CategoryListItem object by category ID."""
    category = load_category_by_id(category_id, session)
    return category


@router.get("/categories/key/{category_key}", response_model=CategoryListItem)
def get_category_by_key(
    category_key: str,
    session: Annotated[Session, Depends(get_session)],
) -> CategoryListItem:
    """Return a single CategoryListItem object by category ID."""
    category = load_category_by_key(category_key, session)
    return category
