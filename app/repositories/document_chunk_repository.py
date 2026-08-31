

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
    ) -> list[DocumentChunk]:

        document_chunks = [
            DocumentChunk(
            document_id=document_id,
            chunk_index=index,
            content=content,
        )
            for index, content in enumerate(chunks)
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