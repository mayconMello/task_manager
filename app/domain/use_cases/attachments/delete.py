from app.core.configs import settings
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.attachment_repository import AttachmentRepository
from app.infra.repositories.task_repository import TaskRepository


class DeleteAttachmentUseCase:
    def __init__(
            self,
            repository: AttachmentRepository,
            repository_task: TaskRepository
    ):
        self.repository = repository
        self.repository_task = repository_task

    async def execute(self, user_id: str, task_id: str, attachment_id: str):
        task = await self.repository_task.get(user_id, task_id)
        if not task:
            raise ResourceNotFoundError(
                "Task not found or you do not have permission to access this task."
            )

        attachment = await self.repository.get(task_id, attachment_id)
        if not attachment:
            raise ResourceNotFoundError("Attachment not found.")

        file_path = settings.storage_full_path / attachment.filename
        file_path.unlink(missing_ok=True)
        await self.repository.delete(task.id, attachment.id)
