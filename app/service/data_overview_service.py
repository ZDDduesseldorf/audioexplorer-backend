from pathlib import Path
import sys
from .json_utils import load_json_file
from fastapi import HTTPException

try:
    from app.schemas.sound import DataOverview
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from app.schemas.sound import DataOverview

### lade alle objekte


def load_all_data_overview():
    BASE_DIR = Path(__file__).resolve().parents[2]
    json_path = BASE_DIR / "data" / "data_overview.json"

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
            anomalie=item["anomalie_isolation_forest"],
            # TODO: weitere Anomaliefelder einfügen
        )
        for uuid, item in data_json.items()
    ]


### lade ein Objekt anhand uuid


def load_data_by_uuid(uuid: str):
    BASE_DIR = Path(__file__).resolve().parents[2]
    json_path = BASE_DIR / "data" / "data_overview.json"

    data_json = load_json_file(json_path)

    data_uuid = data_json[uuid]

    if data_uuid is None:
        raise HTTPException(status_code=404, detail=f"Datapoint {id} not found")

    return DataOverview(
        uuid=uuid,
        umap_x=data_uuid["umap_x"],
        umap_y=data_uuid["umap_y"],
        umap_z=data_uuid["umap_z"],
        label=data_uuid["label"],
        category=data_uuid["category"],
        filename=data_uuid["filename"],
        anomalie=data_uuid["anomalie_isolation_forest"],
        # TODO: weitere Anomaliefelder einfügen
    )
