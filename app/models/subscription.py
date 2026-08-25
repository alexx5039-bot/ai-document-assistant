from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.enum import SubscriptionPlan, SubscriptionStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    stripe_customer_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    stripe_subscription_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    plan: Mapped[str] = mapped_column(
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    status: Mapped[SubscriptionStatus] = mapped_column(
        default=SubscriptionStatus.ACTIVE,
        nullable=False,
    )

    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="subscription"
    )

