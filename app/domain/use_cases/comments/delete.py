from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.comment_repository import CommentRepository
from app.infra.repositories.task_repository import TaskRepository


class DeleteCommentUseCase:
    def __init__(
            self,
            repository: CommentRepository,
            repository_task: TaskRepository
    ):
        self.repository = repository
        self.repository_task = repository_task

    async def execute(self, user_id: str, task_id: str, comment_id: str):
        task = await self.repository_task.get(user_id, task_id)
        if not task:
            raise ResourceNotFoundError(
                "Task not found or you do not have permission to access this task."
            )

        comment = await self.repository.get(task_id, comment_id)
        if not comment:
            raise ResourceNotFoundError("Comment not found.")

        await self.repository.delete(task.id, comment.id)
