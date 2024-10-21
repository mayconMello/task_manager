from pydantic import UUID4

from app.domain.entities.task import Task
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository


class GetTaskUseCase:
    def __init__(
            self,
            repository: TaskRepository,
            repository_user: UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(self, task_id: UUID4, user_id: UUID4) -> Task:
        user = await self.repository_user.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError()

        task = await self.repository.get(
            user.id,
            task_id
        )

        if not task:
            raise ResourceNotFoundError()

        return task
