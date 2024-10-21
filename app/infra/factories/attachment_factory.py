from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.attachments.create import CreateAttachmentUseCase
from app.domain.use_cases.attachments.delete import DeleteAttachmentUseCase
from app.domain.use_cases.attachments.list import ListAttachmentsUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_attachment_repository import SQLAlchemyAttachmentRepository
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import SQLAlchemyTaskRepository


class AttachmentFactory:

    @staticmethod
    def repositories(
            session: AsyncSession,
    ):
        repository = SQLAlchemyAttachmentRepository(session)
        repository_task = SQLAlchemyTaskRepository(session)

        return repository, repository_task

    def create_attachment_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> CreateAttachmentUseCase:
        return CreateAttachmentUseCase(
            *self.repositories(session)
        )

    def list_attachments_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> ListAttachmentsUseCase:
        return ListAttachmentsUseCase(
            *self.repositories(session)
        )

    def delete_attachment_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> DeleteAttachmentUseCase:
        return DeleteAttachmentUseCase(
            *self.repositories(session)
        )
