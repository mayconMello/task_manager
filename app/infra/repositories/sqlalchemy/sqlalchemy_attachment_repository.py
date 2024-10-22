from typing import List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.attachment import Attachment
from app.infra.db.models import AttachmentModel
from app.infra.repositories.attachment_repository import AttachmentRepository


class SQLAlchemyAttachmentRepository(AttachmentRepository):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(self, attachment: Attachment) -> Attachment:
        attachment_db = AttachmentModel(
            original_name=attachment.original_name,
            filename=attachment.filename,
            file_path=attachment.file_path,
            task_id=attachment.task_id,
        )

        self.session.add(attachment_db)
        await self.session.commit()
        await self.session.refresh(attachment_db)

        return Attachment.model_validate(attachment_db)

    async def delete(self, task_id: UUID4, attachment_id: UUID4):
        query = (
            select(AttachmentModel)
            .where(
                AttachmentModel.task_id == task_id,
            )
            .where(AttachmentModel.id == attachment_id)
        )
        result = await self.session.execute(query)

        attachment = result.scalar()

        await self.session.delete(attachment)
        await self.session.commit()

    async def get(self, task_id: UUID4, attachment_id: UUID4) -> Attachment | None:
        query = (
            select(AttachmentModel)
            .where(
                AttachmentModel.task_id == task_id,
            )
            .where(AttachmentModel.id == attachment_id)
        )
        result = await self.session.execute(query)

        attachment = result.scalar_one_or_none()

        if attachment:
            return Attachment.model_validate(attachment)

        return attachment

    async def list(self, task_id: UUID4) -> List[Attachment]:
        query = select(AttachmentModel).where(
            AttachmentModel.task_id == task_id,
        )
        result = await self.session.execute(query)

        attachments = result.scalars().all()

        return list(map(Attachment.model_validate, attachments))
