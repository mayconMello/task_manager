from datetime import datetime, timedelta
from typing import List

from pydantic import UUID4

from app.domain.entities.task import Task
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository


class ListTasksDueSoonUseCase:
    def __init__(
            self,
            repository: TaskRepository,
            repository_user: UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(self, user_id: UUID4) -> List[Task]:
        user = await self.repository_user.get_by_id(
            user_id
        )

        if not user:
            raise ResourceNotFoundError()

        current_time = datetime.now()
        due_time_limit = current_time + timedelta(hours=24)
        tasks = await self.repository.list_due_soon(
            user.id,
            due_time_limit
        )
        return tasks
