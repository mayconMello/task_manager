from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, UUID4

from app.domain.entities.subtask import Subtask

fake = Faker()


class OverrideSubtask(BaseModel):
    id: Optional[UUID4] = None
    title: Optional[str] = None
    is_completed: bool = False
    task_id: Optional[UUID4] = None


def make_subtask(override: OverrideSubtask = OverrideSubtask()) -> Subtask:
    return Subtask(
        id=override.id or uuid4(),
        title=override.title or fake.sentence().title(),
        is_completed=override.is_completed or False,
        task_id=override.task_id or uuid4(),
    )
