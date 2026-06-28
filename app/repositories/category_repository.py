from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import Category
from app.repositories.category_records import CategoryInsertRecord


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

    def find_technical_keys_by_category_keys(
        self,
        category_keys: set[str],
    ) -> dict[str, int]:
        if not category_keys:
            return {}

        statement = select(Category).where(
            Category.category_key.in_(category_keys),
        )

        categories = self.session.scalars(statement).all()

        return {
            category.category_key: category.technical_key for category in categories
        }

    def insert_many(
        self,
        records: Sequence[CategoryInsertRecord],
    ) -> int:
        if not records:
            return 0

        statement = insert(Category).values(list(records))

        try:
            self.session.execute(statement)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

        return len(records)
