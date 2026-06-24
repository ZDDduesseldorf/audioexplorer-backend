import httpx

BASE_URL = "http://127.0.0.1:8000"


def test_openapi_docs_are_reachable() -> None:
    response = httpx.get(f"{BASE_URL}/docs", timeout=5.0)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_data_overviews_via_http() -> None:
    response = httpx.get(f"{BASE_URL}/api/v1/sounds/overviews", timeout=5.0)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["uuid"] == "sample-001"
    assert data[0]["category"] == "laugh"


def test_get_categories_via_http() -> None:
    response = httpx.get(f"{BASE_URL}/api/v1/sounds/categories", timeout=5.0)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["id"] == 1
    assert data[1]["key"] == "cry"
