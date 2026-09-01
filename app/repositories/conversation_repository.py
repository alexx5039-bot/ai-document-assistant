from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Conversation


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id) -> Conversation:
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_by_id(
            self,
            conversation_id: int,
    ) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
        )

        return result.scalar_one_or_none()

    async def get_by_user(
            self,
            user_id: int,
    ) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
        )

        return list(result.scalars().all())
