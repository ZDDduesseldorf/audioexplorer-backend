from pathlib import Path
import sys
from .json_utils import load_json_file
from fastapi import HTTPException
from app.config import get_data_file_path
from app.schemas.sound import DataOverview


### lade alle objekte


def load_all_data_overview(json_path: Path):

    data_json = load_json_file(json_path)

    return [
        DataOverview(
            uuid=uuid,
            umap_x=item["umap_x"],
            umap_y=item["umap_y"],
            umap_z=item["umap_z"],
            label=item["label"],
            category=item["category"],
            filename=item["filename"],
            anomalie_isolation_forest=item["anomalie_isolation_forest"],
            anomalie_LOF=item["anomalie_LOF"],
            anomalie_isolation_forest_label=item["anomalie_isolation_forest_label"],
            anomalie_LOF_label=item["anomalie_LOF_label"],
        )
        for uuid, item in data_json.items()
    ]


### lade ein Objekt anhand uuid


def load_data_by_uuid(uuid: str, json_path):

    data_json = load_json_file(json_path)

    data_uuid = data_json.get(uuid)

    if data_uuid is None:
        raise HTTPException(status_code=404, detail=f"Datapoint {uuid} not found")

    return DataOverview(
        uuid=uuid,
        umap_x=data_uuid["umap_x"],
        umap_y=data_uuid["umap_y"],
        umap_z=data_uuid["umap_z"],
        label=data_uuid["label"],
        category=data_uuid["category"],
        filename=data_uuid["filename"],
        anomalie_isolation_forest=data_uuid["anomalie_isolation_forest"],
        anomalie_LOF=data_uuid["anomalie_LOF"],
        anomalie_isolation_forest_label=data_uuid["anomalie_isolation_forest_label"],
        anomalie_LOF_label=data_uuid["anomalie_LOF_label"],
    )
