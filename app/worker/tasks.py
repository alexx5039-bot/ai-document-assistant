import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_content_repository import DocumentContentRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.file_service import FileService
from app.services.subscription_service import SubscriptionService
from app.services.text_extraction_service import TextExtractionService
from app.worker.celery_app import celery_app

worker_engine = create_async_engine(
    settings.database_url,
    echo=True,
)

WorkerSessionLocal = async_sessionmaker(
    worker_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@celery_app.task
def process_document_task(document_id: int, user_id: int):
    asyncio.run(_process_document(document_id=document_id, user_id=user_id))
    return {
        "document_id": document_id,
        "status": "processed",
    }


async def _process_document(
    document_id: int,
    user_id: int,
):
    async with WorkerSessionLocal() as db:
        document_repo = DocumentRepository(db)
        document_content_repo = DocumentContentRepository(db)
        document_chunk_repo = DocumentChunkRepository(db)
        subscription_repo = SubscriptionRepository(db)

        file_service = FileService()
        text_extraction_service = TextExtractionService()
        chunking_service = ChunkingService()
        embedding_service = EmbeddingService()

        subscription_service = SubscriptionService(
            subscription_repo,
            document_repo,
        )

        document_service = DocumentService(
            document_repo,
            file_service,
            document_content_repo,
            text_extraction_service,
            chunking_service,
            document_chunk_repo,
            embedding_service,
            subscription_service,
        )

        return await document_service.process_document(
            document_id=document_id,
            user_id=user_id,
        )
