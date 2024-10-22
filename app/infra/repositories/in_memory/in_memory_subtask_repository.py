import uuid
from typing import List

from pydantic import UUID4

from app.domain.entities.subtask import Subtask, SubtaskUpdate
from app.infra.repositories.subtask_repository import SubtaskRepository


class InMemorySubtaskRepository(SubtaskRepository):
    def __init__(self):
        self.items: List[Subtask] = []

    async def create(self, subtask: Subtask) -> Subtask:
        subtask.id = subtask.id or uuid.uuid4()
        self.items.append(subtask)

        return subtask

    async def list(self, task_id: UUID4) -> List[Subtask]:
        subtasks = [subtask for subtask in self.items if subtask.task_id == task_id]

        return subtasks

    async def get(self, task_id: UUID4, subtask_id: UUID4) -> Subtask | None:
        for item in self.items:
            if item.task_id == task_id and item.id == subtask_id:
                return item

        return None

    async def delete(self, task_id: UUID4, subtask_id: UUID4):
        for item in self.items:
            if item.task_id == task_id and item.id == subtask_id:
                self.items.remove(item)

    async def update(self, task_id: UUID4, subtask_id: UUID4, subtask: SubtaskUpdate) -> Subtask:
        for index, item in enumerate(self.items):
            if item.task_id == task_id and item.id == subtask_id:
                item.title = subtask.title
                item.is_completed = subtask.is_completed
                self.items[index] = item

                return item

    async def update_all_status(self, task_id: UUID4, is_completed: bool):
        for index, item in enumerate(self.items):
            if item.task_id == task_id:
                item.is_completed = is_completed
                self.items[index] = item
