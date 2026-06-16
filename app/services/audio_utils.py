from app.services.metadata_utils import build_audio_path_from_metadata
from fastapi import HTTPException
import os.path


def find_audio_url_by_uuid(uuid: str):
    audio_url = build_audio_path_from_metadata(uuid)

    if os.path.isfile(audio_url):
        return audio_url
    else:
        raise HTTPException(status_code=404, detail=f"Audio for {uuid} not found")
