from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DocumentContent


class DocumentContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            document_id: int,
            content: str
    ) -> DocumentContent:

        document_content = DocumentContent(
            document_id=document_id,
            content=content,
        )
        self.db.add(document_content)
        await self.db.commit()
        await self.db.refresh(document_content)

        return document_content

    async def get_by_document_id(self, document_id: int) -> DocumentContent | None:
        stmt = select(DocumentContent).where(
            DocumentContent.document_id == document_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
            self,
            document_content: DocumentContent,
            content: str
    ) -> DocumentContent:

        document_content.content = content
        await self.db.commit()
        await self.db.refresh(document_content)
        return document_content