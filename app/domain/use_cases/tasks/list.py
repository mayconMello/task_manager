from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.domain.entities.task import Task
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository


class TaskListFilter(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category_id: Optional[UUID4] = None


class ListTasksUseCase:
    def __init__(
        self,
        repository: TaskRepository,
        repository_user: UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(
        self, user_id: UUID4, params: TaskListFilter = None
    ) -> List[Task]:
        params = params or TaskListFilter()

        user = await self.repository_user.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError()

        tasks = await self.repository.list(
            user.id,
            params.model_dump(exclude_none=True),
        )

        return tasks
