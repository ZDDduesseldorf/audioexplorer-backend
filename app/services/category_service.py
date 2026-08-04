from fastapi import HTTPException

from app.repositories.category_repository import CategoryRepository
from app.schemas.sound import CategoryListItem


def load_all_categories(session) -> list[CategoryListItem]:
    """Load all categories from the category_list.json file and return a list of CategoryListItem objects."""
    service = CategoryRepository(session)

    categories = service.find_all()

    return [
        CategoryListItem(id=item.id, key=item.category_key, name=item.display_name)
        for item in categories
    ]


def load_category_by_id(id: int, session) -> CategoryListItem:
    """Load a single category by ID from the category_list.json file and return a CategoryListItem object."""
    service = CategoryRepository(session)

    category_id = service.find_by_category_id(id)

    if category_id is None:
        raise HTTPException(status_code=404, detail=f"Category {id} not found")

    return CategoryListItem(
        id=category_id.id, key=category_id.category_key, name=category_id.display_name
    )


def load_category_by_key(key: str, session) -> CategoryListItem:
    """Load a single category by ID from the category_list.json file and return a CategoryListItem object."""
    service = CategoryRepository(session)

    category_id = service.find_by_category_key(key)

    if category_id is None:
        raise HTTPException(status_code=404, detail=f"Category {key} not found")

    return CategoryListItem(
        id=category_id.id, key=category_id.category_key, name=category_id.display_name
    )
