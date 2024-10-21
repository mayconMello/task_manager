import os
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.configs import settings
from app.domain.entities.attachment import Attachment
from app.domain.errors import ResourceNotFoundError, MaxFileSizeError
from app.infra.repositories.attachment_repository import AttachmentRepository
from app.infra.repositories.task_repository import TaskRepository


class CreateAttachmentUseCase:
    def __init__(
            self,
            repository: AttachmentRepository,
            repository_task: TaskRepository,
            storage_path: Path = settings.storage_full_path,
    ):
        self.repository = repository
        self.repository_task = repository_task
        self.storage_path = storage_path

    async def execute(self, user_id, task_id: str, file: UploadFile) -> Attachment:
        task = await self.repository_task.get(
            user_id,
            task_id
        )

        if not task:
            raise ResourceNotFoundError(
                "Task not found or you do not have permission to access this task."
            )

        if file.size > settings.max_file_size_bytes:
            raise MaxFileSizeError()

        extention = Path(file.filename).suffix
        filename = f'{str(uuid4())}{extention}'
        file_path = os.path.join(settings.storage_path, filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        attachment = Attachment(
            task_id=task_id,
            original_name=file.filename,
            filename=filename,
            file_path=file_path
        )
        attachment = await self.repository.create(
            attachment
        )
        return attachment
