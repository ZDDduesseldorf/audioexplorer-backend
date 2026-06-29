from typing import TypedDict
from uuid import UUID


class DataOverviewInsertRecord(TypedDict):
    uuid: UUID
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category_technical_key: int
    filename: str
    anomalie_isolation_forest: float
    anomalie_lof: float
    anomalie_lof_label: str
    anomalie_isolation_forest_label: str
    nearest_neighbors: dict[str, float]
