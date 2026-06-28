from typing import TypedDict


class CategoryInsertRecord(TypedDict):
    id: int
    category_key: str
    display_name: str