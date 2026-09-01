from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.ask import SourceResponse
from app.services.llm_service import LLMService
from app.services.search_service import SearchService


class RAGService:
    def __init__(
            self,
            search_service: SearchService,
            llm_service: LLMService,
            conversation_repo: ConversationRepository,
            message_repo: MessageRepository
    ):
        self.search_service = search_service
        self.llm_service = llm_service
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    async def answer(
            self,
            user_id: int,
            conversation_id: int,
            query: str,
            document_id: int | None = None,
            limit: int = 5,
    ) -> str:
        if conversation_id is None:
            conversation = await self.conversation_repo.create(
                user_id=user_id
            )
            conversation_id = conversation.id
        else:
            conversation = await self.conversation_repo.get_by_id(
                conversation_id
            )

            if conversation is None or conversation.user_id != user_id:
                return "", []

        await self.message_repo.create(
            conversation_id=conversation_id,
            role="user",
            content=query,
        )
        history = await self.message_repo.get_by_conversation(
            conversation_id=conversation_id
        )



        results = await self.search_service.search(
            user_id=user_id,
            query=query,
            document_id=document_id,
            limit=limit
        )

        if not results:
            return "", []

        context = "\n\n".join(
            result.content
            for result in results
        )
        history_text = "\n\n".join(
            f"{message.role}:{message.content}"
            for message in history
        )
        answer = await self.llm_service.generate(
            query=query,
            context=context,
            history=history_text,
        )
        await self.message_repo.create(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )
        return answer, results