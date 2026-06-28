from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.data_import import DataOverviewImportResponse
from app.services.data_overview_import_service import (
    DataOverviewImportError,
    DataOverviewImportService,
)

router = APIRouter(
    prefix="/imports",
    tags=["imports"],
)


@router.post("/data-overview", response_model=DataOverviewImportResponse)
async def import_data_overview(
    file: Annotated[UploadFile, File()],
    session: Annotated[Session, Depends(get_session)],
) -> DataOverviewImportResponse:
    if not file.filename or not file.filename.endswith(".npz"):
        raise HTTPException(
            status_code=400,
            detail="Only .npz files are supported.",
        )

    file_content = await file.read()

    service = DataOverviewImportService(session)

    try:
        imported_rows = service.import_npz_file(file_content)
    except DataOverviewImportError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except IntegrityError as error:
        raise HTTPException(
            status_code=409,
            detail=(
                "Import failed because at least one record already exists "
                "or violates a database constraint."
            ),
        ) from error

    return DataOverviewImportResponse(
        imported_rows=imported_rows,
        message="Data overview import completed.",
    )
