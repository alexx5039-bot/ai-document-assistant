from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Document
from app.models.enum import DocumentStatus


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            user_id: int,
            filename: str,
            file_path: str,
    ) -> Document:

        document = Document(
            user_id=user_id,
            filename=filename,
            file_path=file_path
        )
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)

        return document

    async def get_by_id(self, document_id: int, user_id: int) -> Document | None:
        stmt = select(Document).where(
            Document.id == document_id,
            Document.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> list[Document]:
        stmt = select(Document).where(
            Document.user_id == user_id
        ).order_by(Document.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_user(self, user_id: int) -> int:
        stmt = select(func.count(Document.id).where(
            Document.user_id == user_id
        ))
        result = await self.db.execute(stmt)
        return result.scalar_one()


    async def delete(self, document: Document):
        await self.db.delete(document)
        await self.db.commit()

    async def update_status(
            self,
            document: Document,
            status: DocumentStatus
    ) -> Document:
        document.status = status
        await self.db.commit()
        await self.db.refresh(document)

        return document
