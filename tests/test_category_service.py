from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

import app.services.category_service as cat
from app.db.models import Category


def test_load_all_categories():
    session = MagicMock()

    category1 = Category(
        technical_key=1,
        id=1,
        category_key="laugh",
        display_name="lachen",
    )
    category2 = Category(
        technical_key=2,
        id=2,
        category_key="cry",
        display_name="weinen",
    )
    category3 = Category(
        technical_key=3,
        id=3,
        category_key="clap",
        display_name="klatschen",
    )

    repo = MagicMock()

    repo.find_all.return_value = [category1, category2, category3]

    with patch.object(cat, "CategoryRepository", return_value=repo):
        categories = cat.load_all_categories(session)

    assert len(categories) == 3

    item = categories[0]

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id():

    session = MagicMock()

    category1 = Category(
        technical_key=1,
        id=1,
        category_key="laugh",
        display_name="lachen",
    )

    repo = MagicMock()

    repo.find_by_category_id.return_value = category1

    with patch.object(cat, "CategoryRepository", return_value=repo):
        item = cat.load_category_by_id(1, session)

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_id_raises_404_when_missing():

    session = MagicMock()

    repo = MagicMock()

    repo.find_by_category_id.return_value = None
    with (
        patch.object(cat, "CategoryRepository", return_value=repo),
        pytest.raises(HTTPException) as exc_info,
    ):
        cat.load_category_by_id(999, session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category 999 not found"


def test_load_category_by_key():
    session = MagicMock()

    category1 = Category(
        technical_key=1,
        id=1,
        category_key="laugh",
        display_name="lachen",
    )

    repo = MagicMock()

    repo.find_by_category_key.return_value = category1

    with patch.object(cat, "CategoryRepository", return_value=repo):
        item = cat.load_category_by_key("laugh", session)

    assert item.id == 1
    assert item.key == "laugh"
    assert item.name == "lachen"


def test_load_category_by_key_raises_404_when_missing():

    session = MagicMock()

    repo = MagicMock()

    repo.find_by_category_key.return_value = None
    with (
        patch.object(cat, "CategoryRepository", return_value=repo),
        pytest.raises(HTTPException) as exc_info,
    ):
        cat.load_category_by_key("mh", session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Category mh not found"
