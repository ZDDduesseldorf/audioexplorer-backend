import json
from pathlib import Path

from app.main import app


def test_openapi_contract_matches_committed_snapshot() -> None:
    contract_path = Path("api_contract/openapi.json")

    expected_contract = json.loads(contract_path.read_text(encoding="utf-8"))
    current_contract = app.openapi()

    assert current_contract == expected_contract
