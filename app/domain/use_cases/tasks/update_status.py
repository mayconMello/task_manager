from pydantic import UUID4

from app.domain.entities.task import Task
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.subtask_repository import SubtaskRepository
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository


class UpdateStatusTaskUseCase:
    def __init__(
            self,
            repository: TaskRepository,
            repository_user: UserRepository,
            repository_subtask: SubtaskRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user
        self.repository_subtask = repository_subtask

    async def execute(
            self,
            task_id: UUID4,
            user_id: UUID4,
            is_completed: bool,
    ) -> Task:
        user = await self.repository_user.get_by_id(
            user_id
        )

        if not user:
            raise ResourceNotFoundError()

        task = await self.repository.get(
            user.id,
            task_id
        )

        if not task:
            raise ResourceNotFoundError()

        updated_task = await self.repository.update_status(
            task_id,
            is_completed
        )

        if is_completed:
            await self.repository_subtask.update_all_status(
                task.id,
                is_completed
            )

        return updated_task
