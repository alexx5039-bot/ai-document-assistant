from app.models import Subscription
from app.repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:
    def __init__(
            self,
            subscription_repo: SubscriptionRepository
    ):
        self.subscription_repo = subscription_repo

    async def get_or_create(self, user_id: int) -> Subscription:
        subscription = await self.subscription_repo.get_subscription_by_user_id(user_id)
        if subscription is None:
            subscription = await self.subscription_repo.create(user_id)
        return subscription