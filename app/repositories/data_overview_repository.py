from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.db.models import Category, DataOverview
from app.repositories.data_overview_records import DataOverviewInsertRecord


class DataOverviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_all(self) -> list[DataOverview]:
        statement = (
            select(DataOverview)
            .options(joinedload(DataOverview.category))
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_uuid(self, uuid: UUID) -> DataOverview | None:
        statement = (
            select(DataOverview)
            .options(joinedload(DataOverview.category))
            .where(DataOverview.uuid == uuid)
        )
        return self.session.scalars(statement).first()

    def find_by_label(self, label: str) -> list[DataOverview]:
        statement = (
            select(DataOverview)
            .options(joinedload(DataOverview.category))
            .where(DataOverview.label == label)
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_category_key(self, category_key: str) -> list[DataOverview]:
        statement = (
            select(DataOverview)
            .join(DataOverview.category)
            .options(joinedload(DataOverview.category))
            .where(Category.category_key == category_key)
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_anomalie_lof_label(self, anomalie_lof_label: str) -> list[DataOverview]:
        statement = (
            select(DataOverview)
            .options(joinedload(DataOverview.category))
            .where(DataOverview.anomalie_lof_label == anomalie_lof_label)
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_anomalie_isolation_forest_label(
        self,
        anomalie_isolation_forest_label: str,
    ) -> list[DataOverview]:
        statement = (
            select(DataOverview)
            .options(joinedload(DataOverview.category))
            .where(
                DataOverview.anomalie_isolation_forest_label
                == anomalie_isolation_forest_label
            )
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def insert_many(
        self,
        records: Sequence[DataOverviewInsertRecord],
    ) -> int:
        if not records:
            return 0

        statement = insert(DataOverview).values(list(records))

        try:
            self.session.execute(statement)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

        return len(records)
