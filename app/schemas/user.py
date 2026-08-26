from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
