import app.services.data_overview_service as data
from app.config import get_testdata_dir
import pytest
from fastapi import HTTPException


@pytest.fixture
def test_data_overview():
    testdir = get_testdata_dir()
    data_overview_path = testdir / "data_overview.json"
    return data_overview_path


def test_load_all_data_overview(test_data_overview):
    data_overview = data.load_all_data_overview(test_data_overview)

    assert len(data_overview) == 3
    item = data_overview[0]
    assert item.uuid == "sample-001"
    assert item.umap_x == 5.12
    assert item.umap_y == 6.3
    assert item.umap_z == 0
    assert item.label == "laughing"
    assert item.category == "laugh"
    assert item.filename == "a_RA1_01_01__xh6fC2ZfwU_moan.wav"
    assert item.anomalie_isolation_forest == 58.6
    assert item.anomalie_LOF == 59.7
    assert item.anomalie_isolation_forest_label == "unknown"
    assert item.anomalie_LOF_label == "unknown"


def test_load_data_overview_by_uuid(test_data_overview):
    result = data.load_data_by_uuid("sample-001", test_data_overview)

    assert result.uuid == "sample-001"
    assert result.umap_x == 5.12
    assert result.umap_y == 6.3
    assert result.umap_z == 0
    assert result.label == "laughing"
    assert result.category == "laugh"
    assert result.filename == "a_RA1_01_01__xh6fC2ZfwU_moan.wav"
    assert result.anomalie_isolation_forest == 58.6
    assert result.anomalie_LOF == 59.7
    assert result.anomalie_isolation_forest_label == "unknown"
    assert result.anomalie_LOF_label == "unknown"


def test_load_data_by_uuid_raises_404_when_uuid_missing(
    test_data_overview,
):
    with pytest.raises(HTTPException) as exc_info:
        data.load_data_by_uuid(
            "missing-id",
            test_data_overview,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Datapoint missing-id not found"
