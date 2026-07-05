from pydantic import BaseModel


class DataOverviewImportResponse(BaseModel):
    imported_rows: int
    message: str


class CategoryImportResponse(BaseModel):
    imported_rows: int
    message: str
