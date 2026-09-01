from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.subscription import Subscription
    from app.models.conversation import Conversation


class User(Base):
    __tablename__ = "users"


    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    subscription: Mapped["Subscription | None"] = relationship(
       back_populates="user",
       cascade="all, delete-orphan",
       uselist=False
    )

    documents: Mapped[list["Document"]] = relationship(
       back_populates="user",
       cascade="all, delete-orphan",

   )
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )