from fastapi import HTTPException
import os.path
from app.config import get_data_file_path


def find_audio_url_by_uuid(uuid: str):
    """Find the audio file path corresponding to the given UUID."""
    filename = uuid + ".wav"
    audio_path = get_data_file_path(filename)

    if os.path.isfile(audio_path):
        return audio_path
    else:
        raise HTTPException(status_code=404, detail=f"Audio for {uuid} not found")
