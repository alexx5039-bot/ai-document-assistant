
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enum import DocumentStatus

if TYPE_CHECKING:
    from app.models.user import User


class Document(Base):
    __tablename__ = "documents"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    status: Mapped[DocumentStatus] = mapped_column(
        default=DocumentStatus.UPLOADED,
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="documents"
    )
