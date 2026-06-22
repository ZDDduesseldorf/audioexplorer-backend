import app.services.category_service as cat
import pytest
from fastapi import HTTPException


def test_load_all_categories():
    categories = cat.load_all_categories()

    assert len(categories) == 3

    item = categories[0]

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id():
    item = cat.load_category_by_id(
        1,
    )

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id_raises_404_when_missing():
    with pytest.raises(HTTPException) as exc_info:
        cat.load_category_by_id(
            999,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category 999 not found"
