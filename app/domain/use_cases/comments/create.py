from pydantic import UUID4

from app.domain.entities.comment import Comment
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.comment_repository import CommentRepository
from app.infra.repositories.task_repository import TaskRepository


class CreateCommentUseCase:
    def __init__(self, repository: CommentRepository, repository_task: TaskRepository):
        self.repository = repository
        self.repository_task = repository_task

    async def execute(self, user_id: UUID4, task_id: UUID4, body: Comment) -> Comment:
        task = await self.repository_task.get(user_id, task_id)

        if not task:
            raise ResourceNotFoundError(
                "Task not found or you do not have permission to access this task."
            )

        body.task_id = task_id
        body.user_id = user_id
        comment = await self.repository.create(body)

        return comment
