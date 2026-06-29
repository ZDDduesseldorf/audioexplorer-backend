from pydantic import BaseModel, Field


class DataOverview(BaseModel):
    uuid: str
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category: str
    filename: str
    anomalie_isolation_forest: float
    anomalie_LOF: float
    anomalie_isolation_forest_label: str
    anomalie_LOF_label: str
    nearest_neighbors: dict[str, float]


class CategoryListItem(BaseModel):
    id: int
    key: str = Field(description="Stable category identifier")
    name: str = Field(description="Display name of the category")


class LabeledSample(BaseModel):
    uuid: str
    label: str
    category: str
