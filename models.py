from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request body for the /ask endpoint."""

    question: str = Field(min_length=3, max_length=4000)


class Source(BaseModel):
    """Retrieved evidence returned with an answer."""

    source: str
    chunk_id: str
    distance: float | None = None


class AskResponse(BaseModel):
    """Grounded answer plus the evidence used to generate it."""

    answer: str
    sources: list[Source]
    blocked: bool = False
