from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import UUID4

from app.domain.entities.task import Task, TaskUpdate, TaskCreate


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def list(self, user_id: UUID4, params: dict) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def list_due_soon(
        self, due_time_limit: datetime, user_id: Optional[UUID4] = None
    ) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID4, task_id: UUID4) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: UUID4) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_id: UUID4, task: TaskUpdate) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, task_id: UUID4, is_completed: bool) -> Task:
        raise NotImplementedError
