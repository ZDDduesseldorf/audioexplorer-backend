import pytest
import scripts.pipeline as pipe


@pytest.fixture
def sample_metadata_results():
    return {
        "1": {
            "label": "laughing",
            "category": "laugh",
            "filename": "1.wav",
        },
        "2": {
            "label": "crying",
            "category": "cry",
            "filename": "2.wav",
        },
    }


@pytest.fixture
def sample_umap_results():
    return {
        "1": {
            "umap_x": 0.1,
            "umap_y": 0.2,
            "umap_z": 0.3,
        },
        "2": {
            "umap_x": 0.4,
            "umap_y": 0.5,
            "umap_z": 0.6,
        },
    }


@pytest.fixture
def sample_anomaly_results():
    return {
        "1": {
            "anomalie_isolation_forest": -0.1,
            "anomalie_LOF": 1.2,
            "anomalie_label": "normal",
        },
        "2": {
            "anomalie_isolation_forest": -0.8,
            "anomalie_LOF": 2.7,
            "anomalie_label": "anomaly",
        },
    }


def test_create_DataOverview(
    sample_metadata_results, sample_umap_results, sample_anomaly_results
):
    response = pipe.create_DataOverview(
        sample_metadata_results, sample_umap_results, sample_anomaly_results
    )

    assert len(response) == 2
    assert response[0].uuid == "1"
    assert response[0].label == "laughing"
    assert response[0].umap_x == 0.1
    assert response[0].anomalie_LOF == 1.2


# TODO: Add test missing values
