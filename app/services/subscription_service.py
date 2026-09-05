from fastapi import HTTPException, status

from app.models import Subscription
from app.models.enum import SubscriptionPlan
from app.repositories.document_repository import DocumentRepository
from app.repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(
            self,
            subscription_repo: SubscriptionRepository,
            document_repo: DocumentRepository
    ):
        self.subscription_repo = subscription_repo
        self.document_repo = document_repo

    async def get_or_create(self, user_id: int) -> Subscription:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if subscription is None:
            subscription = await self.subscription_repo.create(user_id)
        return subscription

    async def can_upload_document(self, user_id: int) -> bool:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id=user_id)
        quantity = await self.document_repo.count_by_user(user_id=user_id)

        if subscription.plan == SubscriptionPlan.FREE:
            return quantity < 3
        if subscription.plan == SubscriptionPlan.PRO:
            return quantity < 50
        return False

    async def update_plan(self, user_id: int, plan: SubscriptionPlan) -> Subscription:
        subscription = await self.subscription_repo.update_plan(
            user_id=user_id,
            plan=plan
        )
        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found",
            )

        return subscription

