from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.id)
        return list(self.session.scalars(statement).all())

    def find_by_technical_key(self, technical_key: int) -> Category | None:
        statement = select(Category).where(Category.technical_key == technical_key)
        return self.session.scalars(statement).first()

    def find_by_category_key(self, category_key: str) -> Category | None:
        statement = select(Category).where(Category.category_key == category_key)
        return self.session.scalars(statement).first()

    def exists_by_category_key(self, category_key: str) -> bool:
        return self.find_by_category_key(category_key) is not None
