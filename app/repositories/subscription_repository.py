from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Subscription
from app.models.enum import SubscriptionPlan


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            user_id: int,
    ) -> Subscription:
        subscription = Subscription(
            user_id=user_id,
        )

        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription

    async def get_subscription_by_user_id(
            self,
            user_id: int,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription)
            .where(Subscription.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def update_plan(
            self,
            user_id: int,
            plan: SubscriptionPlan
    ) -> Subscription | None:

        subscription = await self.get_subscription_by_user_id(user_id)
        if subscription is None:
            return None
        subscription.plan = plan
        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription