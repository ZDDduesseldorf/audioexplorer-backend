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

    def find_all_umap(self):
        statement = (
            select(
                DataOverview.uuid,
                DataOverview.umap_x,
                DataOverview.umap_y,
                DataOverview.umap_z,
                DataOverview.label,
                Category.category_key.label("category"),
            )
            .join(DataOverview.category)
            .order_by(DataOverview.technical_key)
        )
        return list(self.session.execute(statement).mappings().all())

    def find_all_nn(self):
        statement = select(DataOverview.uuid, DataOverview.nearest_neighbors).order_by(
            DataOverview.technical_key
        )
        return list(self.session.execute(statement).mappings().all())

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

        statement = insert(DataOverview)
        batch_size = 1000

        try:
            for start in range(0, len(records), batch_size):
                batch = list(records[start : start + batch_size])

                self.session.execute(
                    statement,
                    batch,
                )

            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            raise

        return len(records)
