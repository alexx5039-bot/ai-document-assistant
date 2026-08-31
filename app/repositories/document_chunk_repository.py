from pgvector.sqlalchemy import Vector

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentChunk, Document


class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(
            self,
            document_id: int,
            chunks: list[str],
            embeddings: list[list[float]]
    ) -> list[DocumentChunk]:

        document_chunks = [
            DocumentChunk(
            document_id=document_id,
            chunk_index=index,
            content=content,
            embedding=embedding
        )
            for index, (content, embedding) in enumerate(zip(chunks, embeddings))
        ]
        self.db.add_all(document_chunks)
        await self.db.commit()
        return document_chunks


    async def get_by_document_id(self, document_id: int) -> list[DocumentChunk]:
        stmt = (select(DocumentChunk).where(Document.id == document_id)
                .order_by(DocumentChunk.chunk_index.desc()))
        result = await self.db.execute(stmt)
        chunks = result.scalars().all()
        return list(chunks)

    async def delete_by_document_id(self, document_id):
        stmt = delete(DocumentChunk).where(DocumentChunk.document_id == document_id)

        await self.db.execute(stmt)
        await self.db.commit()

    async def search(
            self,
            user_id: int,
            query_embedding: list[float],
            document_id: int | None = None,
            limit: int = 5,
    ):
        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        conditions = [
            Document.user_id == user_id,
            DocumentChunk.embedding.is_not(None)
        ]
        if document_id is not None:
            conditions.append(
                Document.id == document_id
            )

        stmt = (
            select(DocumentChunk, distance)
            .join(Document)
            .where(*conditions)
            .order_by(distance)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.all()