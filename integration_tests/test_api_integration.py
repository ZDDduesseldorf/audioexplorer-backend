import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"


def test_openapi_docs_are_reachable() -> None:
    response = httpx.get(f"{BASE_URL}/docs", timeout=5.0)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.skip(reason="Pending database integration in CI pipeline")
def test_export_labeled_samples_returns_csv() -> None:
    """Test CSV export endpoint returns valid CSV."""
    response = httpx.get(
        f"{BASE_URL}/api/v1/sounds/labeled-samples/export", timeout=5.0
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "charset=utf-8" in response.headers["content-type"].lower()
    assert "attachment" in response.headers.get("content-disposition", "")
