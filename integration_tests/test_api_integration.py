import httpx

BASE_URL = "http://127.0.0.1:8000"


def test_openapi_docs_are_reachable() -> None:
    response = httpx.get(f"{BASE_URL}/docs", timeout=5.0)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
