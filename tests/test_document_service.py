from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, UploadFile

from app.services.document_service import DocumentService


@pytest.mark.asyncio
async def test_create_document_fails_when_upload_limit_reached():
    repo = AsyncMock()
    file_service = AsyncMock()
    content_repo = AsyncMock()
    text_extraction_service = AsyncMock()
    chunking_service = AsyncMock()
    chunks_repo = AsyncMock()
    embedding_service = AsyncMock()
    subscription_service = AsyncMock()

    subscription_service.can_upload_document.return_value = False

    service = DocumentService(
        repo=repo,
        file_service=file_service,
        content_repo=content_repo,
        text_extraction_service=text_extraction_service,
        chunking_service=chunking_service,
        chunks_repo=chunks_repo,
        embedding_service=embedding_service,
        subscription_service=subscription_service,
    )
    file = UploadFile(
        filename="test.pdf",
        file=BytesIO(b"test content"),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.create_document(user_id=1, file=file)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Document upload limit reached"


@pytest.mark.asyncio
async def test_create_document_success():
    repo = AsyncMock()
    file_service = AsyncMock()
    content_repo = AsyncMock()
    text_extraction_service = AsyncMock()
    chunking_service = AsyncMock()
    chunks_repo = AsyncMock()
    embedding_service = AsyncMock()
    subscription_service = AsyncMock()

    subscription_service.can_upload_document.return_value = True
    file_service.save.return_value = "uploads/test.pdf"

    expected_document = object()
    repo.create.return_value = expected_document

    service = DocumentService(
        repo=repo,
        file_service=file_service,
        content_repo=content_repo,
        text_extraction_service=text_extraction_service,
        chunking_service=chunking_service,
        chunks_repo=chunks_repo,
        embedding_service=embedding_service,
        subscription_service=subscription_service,
    )

    file = UploadFile(
        filename="test.pdf",
        file=BytesIO(b"test content"),
    )

    result = await service.create_document(
        user_id=1,
        file=file,
    )

    assert result is expected_document

    subscription_service.can_upload_document.assert_awaited_once_with(1)

    file_service.save.assert_awaited_once_with(file)

    repo.create.assert_awaited_once_with(
        user_id=1,
        filename="test.pdf",
        file_path="uploads/test.pdf",
    )
