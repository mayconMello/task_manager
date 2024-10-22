from typing import List

from pydantic import UUID4

from app.domain.entities.subtask import Subtask
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.subtask_repository import SubtaskRepository
from app.infra.repositories.task_repository import TaskRepository


class ListSubtaskUseCase:
    def __init__(self, repository: SubtaskRepository, repository_task: TaskRepository):
        self.repository = repository
        self.repository_task = repository_task

    async def execute(self, user_id: UUID4, task_id: UUID4) -> List[Subtask]:
        task = await self.repository_task.get(user_id, task_id)

        if not task:
            raise ResourceNotFoundError("Task not found or you do not have permission to access this task.")

        subtasks = await self.repository.list(task_id)

        return subtasks
