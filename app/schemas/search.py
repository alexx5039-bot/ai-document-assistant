from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    document_id: int | None = None
    limit: int = 5

class SearchResult(BaseModel):
    document_id: int
    chunk_index: int
    content: str
    score: float