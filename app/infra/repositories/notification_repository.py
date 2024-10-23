from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, task_id: UUID) -> bool:
        raise NotImplementedError
