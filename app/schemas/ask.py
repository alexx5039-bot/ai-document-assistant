from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    document_id: int | None = None
    limit: int = 5
    conversation_id: int | None = None

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]

class SourceResponse(BaseModel):
    document_id: int
    chunk_index : int
    score: float
