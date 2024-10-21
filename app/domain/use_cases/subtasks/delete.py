from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.subtask_repository import SubtaskRepository
from app.infra.repositories.task_repository import TaskRepository


class DeleteSubtaskUseCase:
    def __init__(
            self,
            repository: SubtaskRepository,
            repository_task: TaskRepository
    ):
        self.repository = repository
        self.repository_task = repository_task

    async def execute(self, user_id: str, task_id: str, subtask_id: str):
        task = await self.repository_task.get(user_id, task_id)
        if not task:
            raise ResourceNotFoundError(
                "Task not found or you do not have permission to access this task."
            )

        subtask = await self.repository.get(task_id, subtask_id)
        if not subtask:
            raise ResourceNotFoundError("Subtask not found.")

        await self.repository.delete(task.id, subtask.id)
