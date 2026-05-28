from pydantic import BaseModel, Field


class DataOverview(BaseModel):
    uuid: str
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category: str
    filename: str
    anomalie: bool | None = None


class CategoryListItem(BaseModel):
    id: str = Field(description="Stable category identifier")
    name: str = Field(description="Display name of the category")


class LabeledSample(BaseModel):
    uuid: str
    label: str
    category: str
