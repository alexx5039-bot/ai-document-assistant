from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enum import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_path: str
    status: DocumentStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
class DocumentStatusUpdate(BaseModel):
    status: DocumentStatus