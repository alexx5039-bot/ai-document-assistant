from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import decode_access_token
from app.db.database import AsyncSessionLocal
from app.models import User
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_content_repository import DocumentContentRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordBearer, oauth2

from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.file_service import FileService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.search_service import SearchService
from app.services.subscription_service import SubscriptionService
from app.services.text_extraction_service import TextExtractionService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_document_repository(db: AsyncSession = Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(db)

async def get_document_content_repository(
        db: AsyncSession = Depends(get_db)
) -> DocumentContentRepository:
    return DocumentContentRepository(db)


async def get_file_service() -> FileService:
    return FileService()

async def get_text_extraction_service() -> TextExtractionService:
    return TextExtractionService()

async def get_chunking_service() -> ChunkingService:
    return ChunkingService()

async def get_document_chunk_repository(
    db: AsyncSession = Depends(get_db),
) -> DocumentChunkRepository:
    return DocumentChunkRepository(db)

_embedding_service = EmbeddingService()

async def get_embedding_service() -> EmbeddingService:
    return _embedding_service

async def get_conversation_repository(
        db: AsyncSession = Depends(get_db)
) -> ConversationRepository:
    return ConversationRepository(db)

async def get_subscription_repository(
        db: AsyncSession = Depends(get_db)
) -> SubscriptionRepository:
    return SubscriptionRepository(db)

async def get_subscription_service(
        repo: SubscriptionRepository = Depends(get_subscription_repository)
) -> SubscriptionService:
    return SubscriptionService(repo)

async def get_user_service(
        repo: UserRepository = Depends(get_user_repository),
        subscription_service: SubscriptionService = Depends(get_subscription_service)
) -> UserService:
    return UserService(repo, subscription_service)


async def get_message_repository(
        db: AsyncSession = Depends(get_db)
) -> MessageRepository:
    return MessageRepository(db)


async def get_llm_service() -> LLMService:
    return LLMService()



async def get_search_service(
        chunk_repo: DocumentChunkRepository = Depends(get_document_chunk_repository),
        embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> SearchService:
    return SearchService(chunk_repo, embedding_service)

async def get_rag_service(
        search_service: SearchService = Depends(get_search_service),
        llm_service: LLMService = Depends(get_llm_service),
        conversation_repo: ConversationRepository = Depends(get_conversation_repository),
        message_repo: MessageRepository = Depends(get_message_repository)
) -> RAGService:
    return RAGService(search_service, llm_service, conversation_repo, message_repo)


async def get_document_service(
        repo: DocumentRepository = Depends(get_document_repository),
        file_service: FileService = Depends(get_file_service),
        text_extraction_service: TextExtractionService = Depends(get_text_extraction_service),
        document_content_repo: DocumentContentRepository = Depends(get_document_content_repository),
        chunking_service: ChunkingService = Depends(get_chunking_service),
        chunk_repository: DocumentChunkRepository = Depends(get_document_chunk_repository),
        embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> DocumentService:
    return DocumentService(
        repo,
        file_service,
        document_content_repo,
        text_extraction_service,
        chunking_service,
        chunk_repository,
        embedding_service,
    )



async def get_current_user(
        token: str = Depends(oauth2_scheme),
        repo: UserRepository = Depends(get_user_repository)
) -> User:

    try:
        user_id = decode_access_token(token)

    except (jwt.InvalidTokenError, KeyError, ValueError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user = await repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    return user
