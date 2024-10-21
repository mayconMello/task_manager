from abc import ABC, abstractmethod
from typing import List

from pydantic import UUID4

from app.domain.entities.subtask import Subtask, SubtaskUpdate


class SubtaskRepository(ABC):

    @abstractmethod
    async def create(self, subtask: Subtask) -> Subtask:
        raise NotImplementedError

    @abstractmethod
    async def list(self, task_id: UUID4) -> List[Subtask]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: UUID4, subtask_id: UUID4) -> Subtask | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: UUID4, subtask_id: UUID4):
        raise NotImplementedError

    @abstractmethod
    async def update(
            self,
            task_id: UUID4,
            subtask_id: UUID4,
            subtask: SubtaskUpdate
    ) -> Subtask:
        raise NotImplementedError

    @abstractmethod
    async def update_all_status(
            self,
            task_id: UUID4,
            is_completed: bool
    ):
        raise NotImplementedError
