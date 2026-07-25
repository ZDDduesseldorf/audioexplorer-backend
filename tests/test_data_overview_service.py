import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock, patch


import app.services.data_overview_service as data
from app.db.models import DataOverview, Category


def test_load_all_data_overview():

    session = MagicMock()

    data1 = DataOverview(
        technical_key=1,
        uuid="sample-001",
        umap_x=5.12,
        umap_y=6.3,
        umap_z=0,
        label="laughing",
        category_technical_key=1,
        original_filename="a_RA1_01_01__xh6fC2ZfwU_moan.wav",
        source="testdata",
        additional_information={
            "context": "baby laugh",
            "location": "",
        },
        anomalie_isolation_forest=58.6,
        anomalie_lof=59.7,
        anomalie_lof_label="unknown",
        anomalie_isolation_forest_label="unknown",
        nearest_neighbors={
            "87654321-4321-8765-4321-876543218765": 0.91,
        },
        category=Category(
            technical_key=1,
            id=1,
            category_key="laugh",
            display_name="lachen",
        ),
    )
    data2 = DataOverview(
        technical_key=1,
        uuid="sample-002",
        umap_x=5.12,
        umap_y=6.3,
        umap_z=0,
        label="laughing",
        category_technical_key=1,
        original_filename="a_RA1_01_01__xh6fC2ZfwU_moan.wav",
        source="testdata",
        additional_information={
            "context": "baby laugh",
            "location": "",
        },
        anomalie_isolation_forest=58.6,
        anomalie_lof=59.7,
        anomalie_lof_label="unknown",
        anomalie_isolation_forest_label="unknown",
        nearest_neighbors={
            "87654321-4321-8765-4321-876543218765": 0.91,
        },
        category=Category(
            technical_key=1,
            id=1,
            category_key="laugh",
            display_name="lachen",
        ),
    )

    repo = MagicMock()

    repo.find_all.return_value = [data1, data2]

    with patch.object(data, "DataOverviewRepository", return_value=repo):
        data_overview = data.load_all_data_overview(session)

    assert len(data_overview) == 2
    item = data_overview[0]
    assert item.uuid == "sample-001"
    assert item.umap_x == 5.12
    assert item.umap_y == 6.3
    assert item.umap_z == 0
    assert item.label == "laughing"
    assert item.category == "laugh"
    assert item.original_filename == "a_RA1_01_01__xh6fC2ZfwU_moan.wav"
    assert item.source == "testdata"
    assert item.additional_information == {
        "context": "baby laugh",
        "location": "",
    }
    assert item.anomalie_isolation_forest == 58.6
    assert item.anomalie_LOF == 59.7
    assert item.anomalie_isolation_forest_label == "unknown"
    assert item.anomalie_LOF_label == "unknown"


def test_load_data_overview_by_uuid():

    session = MagicMock()

    data1 = DataOverview(
        technical_key=1,
        uuid="0a734931-bdd0-4373-946d-eb5220107bff",
        umap_x=5.12,
        umap_y=6.3,
        umap_z=0,
        label="laughing",
        category_technical_key=1,
        original_filename="a_RA1_01_01__xh6fC2ZfwU_moan.wav",
        source="testdata",
        additional_information={
            "context": "baby laugh",
            "location": "",
        },
        anomalie_isolation_forest=58.6,
        anomalie_lof=59.7,
        anomalie_lof_label="unknown",
        anomalie_isolation_forest_label="unknown",
        nearest_neighbors={
            "87654321-4321-8765-4321-876543218765": 0.91,
        },
        category=Category(
            technical_key=1,
            id=1,
            category_key="laugh",
            display_name="lachen",
        ),
    )

    repo = MagicMock()

    repo.find_by_uuid.return_value = data1

    with patch.object(data, "DataOverviewRepository", return_value=repo):
        result = data.load_data_by_uuid("0a734931-bdd0-4373-946d-eb5220107bff", session)

    assert result.uuid == "0a734931-bdd0-4373-946d-eb5220107bff"
    assert result.umap_x == 5.12
    assert result.umap_y == 6.3
    assert result.umap_z == 0
    assert result.label == "laughing"
    assert result.category == "laugh"
    assert result.original_filename == "a_RA1_01_01__xh6fC2ZfwU_moan.wav"
    assert result.source == "testdata"
    assert result.additional_information == {
        "context": "baby laugh",
        "location": "",
    }
    assert result.anomalie_isolation_forest == 58.6
    assert result.anomalie_LOF == 59.7
    assert result.anomalie_isolation_forest_label == "unknown"
    assert result.anomalie_LOF_label == "unknown"


def test_load_data_by_uuid_raises_404_when_uuid_missing():

    session = MagicMock()

    repo = MagicMock()

    repo.find_by_uuid.return_value = None
    with patch.object(data, "DataOverviewRepository", return_value=repo):
        with pytest.raises(HTTPException) as exc_info:
            data.load_data_by_uuid("0a734931-bdd0-4373-946d-eb5220107bff", session)

    assert exc_info.value.status_code == 404
    assert (
        exc_info.value.detail
        == "Datapoint 0a734931-bdd0-4373-946d-eb5220107bff not found"
    )
