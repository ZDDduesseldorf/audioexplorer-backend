from fastapi import APIRouter

from app.schemas.sound import CategoryListItem, DataOverview, LabeledSample

router = APIRouter(
    prefix="/sounds",
    tags=["sounds"],
)


@router.get("/overviews", response_model=list[DataOverview])
def get_all_data_overviews() -> list[DataOverview]:
    return [
        DataOverview(
            uuid="sample-001",
            umap_x=5.12,
            umap_y=6.3,
            umap_z=9.4,
            label="laughing",
            category="laugh",
            filename="a_RA1_01_01__xh6fC2ZfwU_moan.wav",
            anomalie=None,
        ),
        DataOverview(
            uuid="sample-002",
            umap_x=2.4,
            umap_y=1.7,
            umap_z=8.1,
            label="giggle",
            category="laugh",
            filename="b_RA1_01_02__example.wav",
            anomalie=False,
        ),
    ]


@router.get("/overviews/{uuid}", response_model=DataOverview)
def get_data_overview_by_uuid(uuid: str) -> DataOverview:
    return DataOverview(
        uuid=uuid,
        umap_x=5.12,
        umap_y=6.3,
        umap_z=9.4,
        label="laughing",
        category="laugh",
        filename="a_RA1_01_01__xh6fC2ZfwU_moan.wav",
        anomalie=None,
    )


@router.get("/categories", response_model=list[CategoryListItem])
def get_category_list() -> list[CategoryListItem]:
    return [
        CategoryListItem(
            id="laugh",
            name="lachen",
        ),
        CategoryListItem(
            id="speech",
            name="sprache",
        ),
    ]


@router.get("/categories/{category_id}", response_model=CategoryListItem)
def get_category_by_id(category_id: str) -> CategoryListItem:
    return CategoryListItem(
        id=category_id,
        name="lachen",
    )


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
