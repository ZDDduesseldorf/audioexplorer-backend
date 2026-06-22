from pathlib import Path
from .json_utils import load_json_file
from fastapi import HTTPException
from app.schemas.sound import CategoryListItem
from app.config import get_data_file_path


def load_all_categories():
    json_path = get_data_file_path("category_list.json")

    data_json = load_json_file(json_path)

    return [
        CategoryListItem(id=id, key=item["key"], name=item["displayName"])
        for id, item in data_json.items()
    ]


### lade ein Objekt anhand uuid


def load_category_by_id(id: int):
    json_path = get_data_file_path("category_list.json")
    data_json = load_json_file(json_path)

    data_id = data_json.get(str(id))

    if data_id is None:
        raise HTTPException(status_code=404, detail=f"Category {id} not found")

    return CategoryListItem(id=int(id), key=data_id["key"], name=data_id["displayName"])
