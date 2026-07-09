from pydantic import BaseModel, Field


class LabelProposalCreate(BaseModel):
    uuid: str = Field(description="UUID of the sample being labeled")
    category: str = Field(description="Chosen category key, e.g. 'laugh'")


class LabelProposalResponse(BaseModel):
    message: str
