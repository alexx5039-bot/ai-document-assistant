from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import decode_access_token
from app.db.database import AsyncSessionLocal
from app.models import User
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.repositories.document_content_repository import DocumentContentRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordBearer, oauth2

from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.file_service import FileService
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

async def get_user_service(
        repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)

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


async def get_document_service(
        repo: DocumentRepository = Depends(get_document_repository),
        file_service: FileService = Depends(get_file_service),
        text_extraction_service: TextExtractionService = Depends(get_text_extraction_service),
        document_content_repo: DocumentContentRepository = Depends(get_document_content_repository),
        chunking_service: ChunkingService = Depends(get_chunking_service),
        chunk_repository: DocumentChunkRepository = Depends(get_document_chunk_repository)
) -> DocumentService:
    return DocumentService(
        repo,
        file_service,
        document_content_repo,
        text_extraction_service,
        chunking_service,
        chunk_repository
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
