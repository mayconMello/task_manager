from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, ConfigDict


class Notification(BaseModel):
    id: Optional[UUID4] = None
    task_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None
    sent_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
