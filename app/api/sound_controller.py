from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.sound import CategoryListItem, DataOverview, LabeledSample
from app.services.data_overview_service import load_all_data_overview, load_data_by_uuid
from app.services.category_service import load_all_categories, load_category_by_id
from app.services.audio_utils import find_audio_url_by_uuid

router = APIRouter(
    prefix="/sounds",
    tags=["sounds"],
)


@router.get("/overviews", response_model=list[DataOverview])
def get_all_data_overviews() -> list[DataOverview]:
    # Funktion die Liste an DataOverview-Objekten zurückgibt (zuerst laden dieser Daten aus einer lokal gespeicherten JSON-Datei)

    all_data = load_all_data_overview()

    return all_data


@router.get("/overviews/{uuid}", response_model=DataOverview)
def get_data_overview_by_uuid(uuid: str) -> DataOverview:
    # Funktion die ein DataOverview-Objekt zurückgibt, basierend auf der übergebenen UUID
    data_uuid = load_data_by_uuid(uuid)
    return data_uuid


# TODO: Endpunkt der AudioURL übergibt, um die Audiodatei abzuspielen
@router.get("/audio/{uuid}")
def get_audio_by_uuid(uuid: str) -> str:

    audio_path = find_audio_url_by_uuid(uuid)
    return FileResponse(
        path=audio_path, media_type="audio/wav", filename=audio_path.name
    )


@router.get("/categories", response_model=list[CategoryListItem])
def get_category_list() -> list[CategoryListItem]:

    catergory_list = load_all_categories()
    return catergory_list


@router.get("/categories/{category_id}", response_model=CategoryListItem)
def get_category_by_id(category_id: int) -> CategoryListItem:
    category = load_category_by_id(category_id)
    return category


@router.get("/labeled-samples", response_model=list[LabeledSample])
def get_labeled_samples() -> list[LabeledSample]:
    return [
        LabeledSample(
            uuid="sample-001",
            label="giggle",
            category="laugh",
        ),
        LabeledSample(
            uuid="sample-002",
            label="laughing",
            category="laugh",
        ),
    ]


@router.get("/labeled-samples/{uuid}", response_model=LabeledSample)
def get_labeled_sample_by_uuid(uuid: str) -> LabeledSample:
    return LabeledSample(
        uuid=uuid,
        label="giggle",
        category="laugh",
    )
