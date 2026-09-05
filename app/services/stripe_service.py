import stripe

from app.core.config import settings

class StripeService:
    def __init__(self):
        self.client = stripe.StripeClient(
            settings.stripe_secret_key
        )

    async def get_checkout_session(self, session_id: str):
        session = self.client.v1.checkout.sessions.retrieve(session_id)

        print("SESSION ID:", session.id)
        print("STATUS:", session.status)
        print("PAYMENT STATUS:", session.payment_status)
        print("METADATA:", session.metadata)
        print("SUBSCRIPTION:", session.subscription)

        return session

    async def create_checkout_session(self, user_id: int):

        session = self.client.v1.checkout.sessions.create({
            "mode": "subscription",
            "line_items": [
                {
                    "price": settings.stripe_price_id,
                    "quantity": 1,
                }
            ],
            "success_url": "http://localhost:8000/success",
            "cancel_url": "http://localhost:8000/cancel",
            "metadata": {
                "user_id": str(user_id),
            },
        })

        return session