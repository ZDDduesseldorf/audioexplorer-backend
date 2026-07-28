from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Category, DataOverview, LabelProposal


class LabelProposalRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_all(self) -> list[LabelProposal]:
        statement = (
            select(LabelProposal)
            .options(joinedload(LabelProposal.category))
            .order_by(LabelProposal.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_sample_uuid(self, sample_uuid: UUID) -> list[LabelProposal]:
        statement = (
            select(LabelProposal)
            .options(joinedload(LabelProposal.category))
            .where(LabelProposal.sample_uuid == sample_uuid)
            .order_by(LabelProposal.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def save(
        self,
        sample_uuid: UUID,
        category_technical_key: int,
    ) -> LabelProposal:
        label_proposal = LabelProposal(
            sample_uuid=sample_uuid,
            category_technical_key=category_technical_key,
        )

        self.session.add(label_proposal)
        self.session.commit()
        self.session.refresh(label_proposal)

        return label_proposal

    def find_infos_for_csv_export(
        self,
    ) -> list[tuple[LabelProposal, Category, DataOverview]]:
        from app.db.models import Category, DataOverview

        statement = (
            select(LabelProposal, Category, DataOverview)
            .join(
                Category, LabelProposal.category_technical_key == Category.technical_key
            )
            .join(DataOverview, LabelProposal.sample_uuid == DataOverview.uuid)
            .order_by(LabelProposal.created_at.desc())
        )
        result = self.session.execute(statement)
        return [tuple(row) for row in result]
