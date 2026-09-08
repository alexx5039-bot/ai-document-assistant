from pydantic import BaseModel

from app.models.enum import SubscriptionPlan, SubscriptionStatus
from app.models.subscription import Subscription


class SubscriptionResponse(BaseModel):
    plan: SubscriptionPlan
    status: SubscriptionStatus
    documents_used: int
    documents_limit: int
