from datetime import datetime, timedelta
from typing import Optional, Literal
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, UUID4

from app.domain.entities.task import Task, TaskCreate

fake = Faker()


class OverrideTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[Literal['very_low', 'low', 'medium', 'high', 'very_high']] = None
    user_id: Optional[UUID4] = None
    category_id: Optional[UUID4] = None


def make_task(override: OverrideTask = OverrideTask()) -> TaskCreate:
    return TaskCreate(
        title=override.title or fake.sentence().title(),
        description=override.description or fake.text(),
        due_date=override.due_date or datetime.now() + timedelta(days=1),
        priority=override.priority or 'medium',
        user_id=override.user_id or uuid4(),
        category_id=override.category_id or uuid4(),
    )
