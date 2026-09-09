from pydantic import BaseModel

from app.models.enum import SubscriptionPlan, SubscriptionStatus


class SubscriptionResponse(BaseModel):
    plan: SubscriptionPlan
    status: SubscriptionStatus
    documents_used: int
    documents_limit: int
