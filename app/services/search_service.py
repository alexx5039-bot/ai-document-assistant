from sqlalchemy import select

from app.models import DocumentChunk, Document
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.schemas.search import SearchResult
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(
            self,
            chunk_repo: DocumentChunkRepository,
            embedding_service: EmbeddingService
    ):
        self.chunk_repo = chunk_repo
        self.embedding_service = embedding_service

    async def search(
            self,
            user_id: int,
            query: str,
            document_id: int | None = None,
            limit: int = 5,
    ) -> list[SearchResult]:
        query_embedding = self.embedding_service.embed(query)

        results = await self.chunk_repo.search(
            user_id=user_id,
            document_id=document_id,
            query_embedding=query_embedding,
            limit=limit,
        )

        return [
            SearchResult(
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                score=1 - distance,
            )
            for chunk, distance in results
        ]