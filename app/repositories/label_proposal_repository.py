from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Category, LabelProposal


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

    def find_by_user_id(self, user_id: str) -> list[LabelProposal]:
        statement = (
            select(LabelProposal)
            .options(joinedload(LabelProposal.category))
            .where(LabelProposal.user_id == user_id)
            .order_by(LabelProposal.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def find_by_file_hash(self, file_hash: str) -> list[LabelProposal]:
        statement = (
            select(LabelProposal)
            .options(joinedload(LabelProposal.category))
            .where(LabelProposal.file_hash == file_hash)
            .order_by(LabelProposal.technical_key)
        )
        return list(self.session.scalars(statement).all())

    def save(
        self,
        user_id: str,
        file_hash: str,
        category_key: str,
        display_name: str,
    ) -> LabelProposal:
        category_statement = select(Category).where(
            Category.category_key == category_key
        )
        category = self.session.scalars(category_statement).first()

        if category is None:
            raise ValueError(
                f"Category with category_key '{category_key}' does not exist."
            )

        label_proposal = LabelProposal(
            user_id=user_id,
            file_hash=file_hash,
            category_technical_key=category.technical_key,
            display_name=display_name,
        )

        self.session.add(label_proposal)
        self.session.commit()
        self.session.refresh(label_proposal)

        return label_proposal
