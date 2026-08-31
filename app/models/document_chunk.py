from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, UniqueConstraint

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
if TYPE_CHECKING:
    from app.models.document import Document

class DocumentChunk(Base):
    __tablename__ = "document_chunk"

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk_index",
        ),
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(nullable=False)
    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=True
    )


    document: Mapped[Document] = relationship(
        back_populates="chunks"
    )