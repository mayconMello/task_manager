from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, ConfigDict


class Comment(BaseModel):
    id: Optional[UUID4] = None
    content: str
    created_at: Optional[datetime] = None
    task_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None

    model_config = ConfigDict(
        from_attributes=True
    )
