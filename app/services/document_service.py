from fastapi import HTTPException, status, UploadFile

from app.models import Document
from app.models.enum import DocumentStatus
from app.repositories.document_content_repository import DocumentContentRepository
from app.repositories.document_repository import DocumentRepository
from app.services.file_service import FileService
from app.services.text_extraction_service import TextExtractionService


class DocumentService:
    def __init__(
            self,
            repo: DocumentRepository,
            file_service: FileService,
            content_repo: DocumentContentRepository,
            text_extraction_service: TextExtractionService
    ):
        self.repo = repo
        self.file_service = file_service
        self.content_repo = content_repo
        self.text_extraction_service = text_extraction_service


    async def create_document(
            self,
            user_id: int,
            file: UploadFile,
    ) -> Document:
        file_path = await self.file_service.save(file)

        return await self.repo.create(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path
        )

    async def get_document_by_id(
            self,
            document_id: int,
            user_id: int
    ) -> Document | None:
        document = await self.repo.get_by_id(
            document_id=document_id,
            user_id=user_id
        )
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document is not found"
            )
        return document

    async def get_documents(
            self,
            user_id: int
    ) -> list[Document]:
        documents = await self.repo.get_by_user(
             user_id=user_id
        )

        return documents

    async def update_document_status(
            self,
            document_id: int,
            user_id: int,
            document_status: DocumentStatus
    ) -> Document:

        document = await self.repo.get_by_id(
            document_id=document_id,
            user_id=user_id
        )
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document is not found"
            )
        return await self.repo.update_status(document, document_status)


    async def delete_document(self, document_id: int, user_id: int) -> None:

        document = await self.repo.get_by_id(
            document_id=document_id,
            user_id=user_id
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document is not found"
            )
        await self.repo.delete(document)

    async def process_document(
            self,
            document_id: int,
            user_id: int,
    ) -> Document:

        document = await self.repo.get_by_id(
            document_id=document_id,
            user_id=user_id,
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document is not found",
            )

        await self.repo.update_status(
            document,
            DocumentStatus.PROCESSING,
        )

        try:
            content = await self.text_extraction_service.extract(
                document.file_path,
            )

            existing_content = await self.content_repo.get_by_document_id(
                document.id,
            )

            if existing_content:
                await self.content_repo.update(
                    existing_content,
                    content,
                )
            else:
                await self.content_repo.create(
                    document_id=document.id,
                    content=content,
                )

            return await self.repo.update_status(
                document=document,
                status=DocumentStatus.READY,
            )

        except Exception:
            await self.repo.update_status(
                document=document,
                status=DocumentStatus.FAILED,
            )
            raise