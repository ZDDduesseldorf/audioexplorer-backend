from pathlib import Path
import sys
from .json_utils import load_json_file
from fastapi import HTTPException


try:
    from app.schemas.sound import CategoryListItem
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from app.schemas.sound import CategoryListItem


def load_all_categories():
    BASE_DIR = Path(__file__).resolve().parents[2]
    json_path = BASE_DIR / "data" / "category_list.json"

    data_json = load_json_file(json_path)

    return [
        CategoryListItem(id=id, key=item["key"], name=item["displayName"])
        for id, item in data_json.items()
    ]


### lade ein Objekt anhand uuid


def load_category_by_id(id: int):
    BASE_DIR = Path(__file__).resolve().parents[2]
    json_path = BASE_DIR / "data" / "category_list.json"

    data_json = load_json_file(json_path)

    data_id = data_json.get(str(id))

    if data_id is None:
        raise HTTPException(status_code=404, detail=f"Category {id} not found")

    return CategoryListItem(id=id, key=data_id["key"], name=data_id["displayName"])
