from typing import List
from uuid import UUID, uuid4

from app.domain.entities.notification import Notification
from app.infra.repositories.notification_repository import NotificationRepository


class InMemoryNotificationRepository(NotificationRepository):
    def __init__(self):
        self.items: List[Notification] = []

    async def create(self, notification: Notification) -> Notification:
        notification.id = uuid4()
        self.items.append(notification)

        return notification

    async def exists(self, task_id: UUID) -> bool:
        for notification in self.items:
            if notification.task_id == task_id:
                return True

        return False
