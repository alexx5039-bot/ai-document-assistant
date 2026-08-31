from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str
    document_id: int | None = None
    limit: int = 5

class AskResponse(BaseModel):
    answer: str

