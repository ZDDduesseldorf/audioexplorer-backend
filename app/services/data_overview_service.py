from uuid import UUID

from fastapi import HTTPException

from app.repositories.data_overview_repository import DataOverviewRepository
from app.schemas.sound import DataOverviewResponse, Nearest_Neighbours, UMAPResponse


def load_all_data_overview(session) -> list[DataOverviewResponse]:
    """Load all data overviews from the data_overview.json file and return a list of DataOverview objects."""
    service = DataOverviewRepository(session)

    all_data = service.find_all()

    return [
        DataOverviewResponse(
            uuid=str(item.uuid),
            umap_x=item.umap_x,
            umap_y=item.umap_y,
            umap_z=item.umap_z,
            label=item.label,
            category=item.category.category_key,
            original_filename=item.original_filename,
            source=item.source,
            additional_information=item.additional_information,
            anomalie_isolation_forest=item.anomalie_isolation_forest,
            anomalie_LOF=item.anomalie_lof,
            anomalie_isolation_forest_label=item.anomalie_isolation_forest_label,
            anomalie_LOF_label=item.anomalie_lof_label,
            nearest_neighbors=item.nearest_neighbors,
        )
        for item in all_data
    ]


def load_all_umap(session) -> list[UMAPResponse]:
    """Load all data overviews from the data_overview.json file and return a list of DataOverview objects."""
    service = DataOverviewRepository(session)

    all_data = service.find_all_umap()

    return [
        UMAPResponse(
            uuid=str(item["uuid"]),
            umap_x=item["umap_x"],
            umap_y=item["umap_y"],
            umap_z=item["umap_z"],
            label=item["label"],
            category=item["category"],
        )
        for item in all_data
    ]


def load_all_nn(session) -> list[Nearest_Neighbours]:
    service = DataOverviewRepository(session)

    all_data = service.find_all_nn()

    return [
        Nearest_Neighbours(
            uuid=str(item["uuid"]),
            nearest_neighbors=item["nearest_neighbors"],
        )
        for item in all_data
    ]


def load_data_by_uuid(uuid: str, session) -> DataOverviewResponse:
    """Load a single data overview by UUID from the data_overview.json file and return a DataOverview object."""
    service = DataOverviewRepository(session)

    try:
        uuid_obj = UUID(uuid)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"{uuid} is no vaild UUID")

    data_uuid = service.find_by_uuid(uuid_obj)

    if data_uuid is None:
        raise HTTPException(status_code=404, detail=f"Datapoint {uuid_obj} not found")

    return DataOverviewResponse(
        uuid=str(data_uuid.uuid),
        umap_x=data_uuid.umap_x,
        umap_y=data_uuid.umap_y,
        umap_z=data_uuid.umap_z,
        label=data_uuid.label,
        category=data_uuid.category.category_key,
        original_filename=data_uuid.original_filename,
        source=data_uuid.source,
        additional_information=data_uuid.additional_information,
        anomalie_isolation_forest=data_uuid.anomalie_isolation_forest,
        anomalie_LOF=data_uuid.anomalie_lof,
        anomalie_isolation_forest_label=data_uuid.anomalie_isolation_forest_label,
        anomalie_LOF_label=data_uuid.anomalie_lof_label,
        nearest_neighbors=data_uuid.nearest_neighbors,
    )
