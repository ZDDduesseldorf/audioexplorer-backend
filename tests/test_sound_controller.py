from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_data_overviews_returns_two_items() -> None:
    response = client.get("/api/v1/sounds/overviews")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["uuid"] == "sample-001"
    assert data[0]["label"] == "laughing"
    assert data[0]["category"] == "laugh"


def test_get_data_overview_by_uuid_returns_requested_uuid() -> None:
    sample_uuid = "sample-123"

    response = client.get(f"/api/v1/sounds/overviews/{sample_uuid}")

    assert response.status_code == 200

    data = response.json()

    assert data["uuid"] == sample_uuid
    assert data["label"] == "laughing"
    assert data["category"] == "laugh"
    assert data["filename"] == "a_RA1_01_01__xh6fC2ZfwU_moan.wav"


def test_get_category_list_returns_categories() -> None:
    response = client.get("/api/v1/sounds/categories")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "laugh"
    assert data[0]["name"] == "lachen"
    assert data[1]["id"] == "speech"


def test_get_category_by_id_returns_requested_category_id() -> None:
    category_id = "laugh"

    response = client.get(f"/api/v1/sounds/categories/{category_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == category_id
    assert data["name"] == "lachen"


def test_get_labled_samples_returns_two_items() -> None:
    response = client.get("/api/v1/sounds/labeled-samples")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["uuid"] == "sample-001"
    assert data[0]["label"] == "giggle"
    assert data[0]["category"] == "laugh"


def test_get_labled_sample_by_uuid_returns_requested_uuid() -> None:
    sample_uuid = "sample-123"

    response = client.get(f"/api/v1/sounds/labeled-samples/{sample_uuid}")

    assert response.status_code == 404

    data = response.json()

    assert data["uuid"] == sample_uuid
    assert data["label"] == "giggle"
    assert data["category"] == "laugh"
