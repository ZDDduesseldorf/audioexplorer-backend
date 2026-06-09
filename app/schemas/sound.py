from pydantic import BaseModel, Field


# TODO: Anomaly ergänzen
class DataOverview(BaseModel):
    uuid: str
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category: str
    filename: str
    anomalie: float


class CategoryListItem(BaseModel):
    id: int
    key: str = Field(description="Stable category identifier")
    name: str = Field(description="Display name of the category")


class LabeledSample(BaseModel):
    uuid: str
    label: str
    category: str
