import uuid
from typing import List

from pydantic import UUID4

from app.domain.entities.attachment import Attachment
from app.infra.repositories.attachment_repository import AttachmentRepository


class InMemoryAttachmentRepository(AttachmentRepository):
    def __init__(self):
        self.items: List[Attachment] = []

    async def create(self, attachment: Attachment) -> Attachment:
        attachment.id = attachment.id or uuid.uuid4()
        self.items.append(attachment)
        return attachment

    async def list(self, task_id: UUID4) -> List[Attachment]:
        attachments = [attachment for attachment in self.items if attachment.task_id == task_id]

        return attachments

    async def get(self, task_id: UUID4, attachment_id: UUID4) -> Attachment | None:
        for item in self.items:
            if item.task_id == task_id and item.id == attachment_id:
                return item

        return None

    async def delete(self, task_id: UUID4, attachment_id: UUID4):
        for item in self.items:
            if item.task_id == task_id and item.id == attachment_id:
                self.items.remove(item)
                return
