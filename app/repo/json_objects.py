from pydantic import BaseModel
from pathlib import Path


class DataOverviewJSON(BaseModel):
    uuid: str
    umap_x: float
    umap_y: float
    umap_z: float
    label: str
    category: str
    filename: str
    anomalie_isolation_forest: float
    anomalie_LOF: float
    anomalie_label: str


class AudioData(BaseModel):
    uuid: str
    file_path: Path
    audio: list[float]


class PreprocessedAudio(BaseModel):
    uuid: str
    audio: list[float]


class EmbeddingData(BaseModel):
    uuid: str
    embedding: list[float]
