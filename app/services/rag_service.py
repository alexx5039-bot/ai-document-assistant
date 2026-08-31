from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class RAGService:
    def __init__(
            self,
            search_service: SearchService,
            llm_service: LLMService,
    ):
        self.search_service = search_service
        self.llm_service = llm_service

    async def answer(
            self,
            user_id: int,
            query: str,
            document_id: int | None = None,
            limit: int = 5,
    ) -> str:

        results = await self.search_service.search(
            user_id=user_id,
            query=query,
            document_id=document_id,
            limit=limit
        )
        if not results:
            return "I couldn't find relevant information in the documents."

        context = "\n\n".join(
            result.content
            for result in results
        )
        return await self.llm_service.generate(
            query=query,
            context=context,
        )
