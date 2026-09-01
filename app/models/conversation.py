from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models import User
from app.models import Message


class Conversation(Base):
    __tablename__ = "conversations"

    user_id: Mapped[User] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user: Mapped[User] = relationship(
        back_populates="conversations"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Messages.created_at",
    )
