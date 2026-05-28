import json
from pathlib import Path

from app.main import app


def main() -> None:
    output_path = Path("api_contract/openapi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    openapi_schema = app.openapi()

    output_path.write_text(
        json.dumps(openapi_schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"OpenAPI contract exported to {output_path}")


if __name__ == "__main__":
    main()
