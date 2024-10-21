from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, UUID4

from app.domain.entities.comment import Comment

fake = Faker()


class OverrideComment(BaseModel):
    id: Optional[UUID4] = None
    content: Optional[str] = None
    task_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None


def make_comment(override: OverrideComment = OverrideComment()) -> Comment:
    return Comment(
        id=override.id or uuid4(),
        content=override.content or fake.text(),
        created_at=datetime.now(),
        task_id=override.task_id or uuid4(),
        user_id=override.user_id or uuid4(),
    )
