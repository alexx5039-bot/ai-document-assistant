import stripe
from fastapi import APIRouter, Depends, Request, HTTPException, status

from app.db.dependencies import get_stripe_service, get_current_user, get_subscription_service
from app.models import User
from app.models.enum import SubscriptionPlan
from app.services.stripe_service import StripeService
from app.core.config import settings
from app.services.subscription_service import SubscriptionService

router = APIRouter()


@router.post("/checkout")
async def create_checkout(
        service: StripeService = Depends(get_stripe_service),
        current_user: User = Depends(get_current_user),
):
    session = await service.create_checkout_session(
        user_id=current_user.id
    )
    return {
        "checkout_url": session.url
    }

@router.post("/webhooks/stripe")
async def stripe_webhook(
        request: Request,
        service: SubscriptionService = Depends(get_subscription_service),
):
    payload = await request.body()
    signature = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            settings.stripe_webhook_secret,
        )
    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Invalid payload",
        )
    except stripe.SignatureVerificationError:

        raise HTTPException(
            status_code=400,
            detail="Invalid signature",
        )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = int(session.metadata["user_id"])

        await service.update_plan(
            user_id=user_id,
            plan=SubscriptionPlan.PRO,
        )

    return {"status": "success"}

