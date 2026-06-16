import json
from pathlib import Path


### load json data from file
def load_json_file(file_path: Path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


### write json


# TODO: prüfen ob passt
def write_json_file(target_path: Path, data: dict):

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
