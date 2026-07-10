from unittest.mock import MagicMock

import pytest

from app.services import label_proposal_service
from app.services.label_proposal_service import (
    LabelProposalError,
    LabelProposalService,
)

VALID_UUID = "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"


def _build_service(monkeypatch, *, sample_found, category):
    """Build a service whose repositories are replaced by fakes (no real DB)."""
    data_overview_repo = MagicMock()
    data_overview_repo.find_by_uuid.return_value = object() if sample_found else None

    category_repo = MagicMock()
    category_repo.find_by_category_key.return_value = category

    label_proposal_repo = MagicMock()

    monkeypatch.setattr(
        label_proposal_service,
        "DataOverviewRepository",
        lambda session: data_overview_repo,
    )
    monkeypatch.setattr(
        label_proposal_service,
        "CategoryRepository",
        lambda session: category_repo,
    )
    monkeypatch.setattr(
        label_proposal_service,
        "LabelProposalRepository",
        lambda session: label_proposal_repo,
    )

    service = LabelProposalService(session=None)
    return service, label_proposal_repo


def test_rejects_invalid_uuid(monkeypatch):
    service, repo = _build_service(monkeypatch, sample_found=True, category=MagicMock())

    with pytest.raises(LabelProposalError):
        service.create_label_proposal(uuid="not-a-uuid", category_key="laugh")

    repo.save.assert_not_called()


def test_rejects_unknown_sample(monkeypatch):
    service, repo = _build_service(
        monkeypatch, sample_found=False, category=MagicMock()
    )

    with pytest.raises(LabelProposalError):
        service.create_label_proposal(uuid=VALID_UUID, category_key="laugh")

    repo.save.assert_not_called()


def test_rejects_unknown_category(monkeypatch):
    service, repo = _build_service(monkeypatch, sample_found=True, category=None)

    with pytest.raises(LabelProposalError):
        service.create_label_proposal(uuid=VALID_UUID, category_key="banana")

    repo.save.assert_not_called()


def test_saves_valid_proposal(monkeypatch):
    category = MagicMock()
    category.technical_key = 1

    service, repo = _build_service(monkeypatch, sample_found=True, category=category)

    service.create_label_proposal(uuid=VALID_UUID, category_key="laugh")

    repo.save.assert_called_once()
