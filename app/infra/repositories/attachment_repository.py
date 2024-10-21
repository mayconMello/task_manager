from abc import ABC, abstractmethod
from typing import List

from pydantic import UUID4

from app.domain.entities.attachment import Attachment


class AttachmentRepository(ABC):

    @abstractmethod
    async def create(self, attachment: Attachment) -> Attachment:
        raise NotImplementedError

    @abstractmethod
    async def list(self, task_id: UUID4) -> List[Attachment]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: UUID4, attachment_id: UUID4) -> Attachment | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: UUID4, attachment_id: UUID4):
        raise NotImplementedError
