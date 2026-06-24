from app.services.audio_utils import find_audio_url_by_uuid
import pytest
from fastapi import HTTPException
from pathlib import Path


def test_find_audio_url_by_uuid():
    audio_url = find_audio_url_by_uuid("sample-001")

    excepted_path = Path("testdata/sample-001.wav")

    assert audio_url == excepted_path


def test_find_audio_url_by_uuid_raises_404_when_file_not_exists():
    uuid = "1234"

    with pytest.raises(HTTPException) as exc_info:
        find_audio_url_by_uuid(uuid)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Audio for {uuid} not found"
