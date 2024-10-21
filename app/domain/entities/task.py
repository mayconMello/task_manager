from datetime import datetime
from typing import Optional, Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator, UUID4


class Task(BaseModel):
    id: Optional[UUID4] = None
    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID4] = None
    priority: Optional[Literal['low', 'medium', 'high']] = 'medium'
    is_completed: bool = False
    user_id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=False
    )


class TaskCreate(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID4] = None
    priority: Optional[Literal['low', 'medium', 'high']] = 'medium'
    is_completed: bool = False
    user_id: Optional[UUID4] = None

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, due_date: datetime) -> datetime | ValueError:
        if due_date.replace(tzinfo=ZoneInfo('UTC')) <= datetime.now(tz=ZoneInfo('UTC')):
            raise ValueError('Due date cannot be in the past')

        return due_date


class TaskUpdate(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID4] = None
    priority: Optional[Literal['low', 'medium', 'high']] = 'medium'
    is_completed: bool = False


    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, due_date: datetime) -> datetime | ValueError:
        if due_date.replace(tzinfo=ZoneInfo('UTC')) <= datetime.now(tz=ZoneInfo('UTC')):
            raise ValueError('Due date cannot be in the past')

        return due_date

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=False
    )


class TaskUpdateStatus(BaseModel):
    is_completed: bool
