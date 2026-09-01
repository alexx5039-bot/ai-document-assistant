from fastapi import APIRouter, UploadFile, File, Depends, status

from app.db.dependencies import get_current_user, get_document_service, get_search_service, get_rag_service
from app.models import User, Document
from app.schemas.ask import AskResponse, AskRequest, SourceResponse

from app.schemas.document import DocumentResponse, DocumentStatusUpdate
from app.schemas.search import SearchRequest, SearchResult
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.services.search_service import SearchService

router = APIRouter()

@router.post("",
             response_model=DocumentResponse,
             status_code=status.HTTP_201_CREATED
             )
async def create_document(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        service: DocumentService = Depends(get_document_service)
) -> Document:
    return await service.create_document(
        user_id=current_user.id,
        file=file
    )

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK
)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
) -> Document | None:
    return await service.get_document_by_id(
        document_id=document_id,
        user_id=current_user.id
    )

@router.get(
    "",
    response_model=list[DocumentResponse],
    status_code=status.HTTP_200_OK
)
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
) -> list[Document]:
    return await service.get_documents(
        user_id=current_user.id
    )

@router.patch(
    "/{document_id}/status",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK
)
async def update_document_status(
    document_id: int,
    data: DocumentStatusUpdate,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
) -> Document:
    return await service.update_document_status(
        document_id=document_id,
        user_id=current_user.id,
        document_status=data.status
    )

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
) -> None:
    await service.delete_document(
        document_id=document_id,
        user_id=current_user.id,
    )

@router.post(
    "/{document_id}/process",
    response_model=DocumentResponse
)
async def process_document(
        document_id: int,
        current_user: User = Depends(get_current_user),
        service: DocumentService = Depends(get_document_service)
) -> Document:
    return await service.process_document(
        document_id=document_id,
        user_id=current_user.id
    )

@router.post(
    "/search",
    response_model=list[SearchResult]
)
async def search_documents(
        data: SearchRequest,
        current_user: User = Depends(get_current_user),
        service: SearchService = Depends(get_search_service)
):
    return await service.search(
        user_id=current_user.id,
        query=data.query,
        document_id=data.document_id,
        limit=data.limit
    )

@router.post(
    "/ask/",
    response_model=AskResponse
)
async def ask(
        data: AskRequest,
        current_user: User = Depends(get_current_user),
        service: RAGService = Depends(get_rag_service)
):
    answer, results = await service.answer(
        user_id=current_user.id,
        query=data.query,
        document_id=data.document_id,
        limit=data.limit
    )
    sources = [
        SourceResponse(
            document_id=result.document_id,
            chunk_index=result.chunk_index,
            score=result.score,
        )
        for result in results
    ]
    return AskResponse(
        answer=answer,
        sources=sources,
        )