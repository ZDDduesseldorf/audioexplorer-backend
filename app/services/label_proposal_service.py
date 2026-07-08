from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import LabelProposal
from app.repositories.category_repository import CategoryRepository
from app.repositories.data_overview_repository import DataOverviewRepository
from app.repositories.label_proposal_repository import LabelProposalRepository


class LabelProposalError(Exception):
    pass


class LabelProposalService:
    def __init__(self, session: Session) -> None:
        self.category_repository = CategoryRepository(session)
        self.data_overview_repository = DataOverviewRepository(session)
        self.label_proposal_repository = LabelProposalRepository(session)

    def create_label_proposal(
        self,
        uuid: str,
        category_key: str,
    ) -> LabelProposal:
        sample_uuid = self._parse_uuid(uuid)

        if self.data_overview_repository.find_by_uuid(sample_uuid) is None:
            raise LabelProposalError(f"Sample '{uuid}' does not exist.")

        category = self.category_repository.find_by_category_key(category_key)

        if category is None:
            raise LabelProposalError(f"Category '{category_key}' does not exist.")

        return self.label_proposal_repository.save(
            sample_uuid=sample_uuid,
            category_technical_key=category.technical_key,
        )

    def _parse_uuid(self, uuid: str) -> UUID:
        try:
            return UUID(uuid)
        except ValueError as error:
            raise LabelProposalError(f"Invalid UUID: '{uuid}'.") from error
