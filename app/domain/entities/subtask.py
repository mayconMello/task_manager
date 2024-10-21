from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, UUID4


class Subtask(BaseModel):
    id: Optional[UUID4] = None
    title: str = Field(max_length=100)
    is_completed: bool = False
    task_id: Optional[UUID4] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class SubtaskUpdate(BaseModel):
    title: str = Field(max_length=100)
    is_completed: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )