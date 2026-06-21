import app.services.category_service as cat
from app.config import get_testdata_dir
import pytest
from fastapi import HTTPException


@pytest.fixture
def test_category_list():
    testdir = get_testdata_dir()
    category_list = testdir / "category_list.json"
    return category_list


def test_load_all_categories(test_category_list):
    categories = cat.load_all_categories(test_category_list)

    assert len(categories) == 3

    item = categories[0]

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id(test_category_list):
    item = cat.load_category_by_id(
        1,
        test_category_list,
    )

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id_raises_404_when_missing(test_category_list):
    with pytest.raises(HTTPException) as exc_info:
        cat.load_category_by_id(
            999,
            test_category_list,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category 999 not found"
