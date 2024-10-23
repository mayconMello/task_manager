from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.notification import Notification
from app.infra.db.models import NotificationModel
from app.infra.repositories.notification_repository import NotificationRepository


class SQLAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        db_notification = NotificationModel(
            task_id=notification.task_id,
            user_id=notification.user_id,
            sent_at=notification.sent_at,
        )

        self.session.add(db_notification)
        await self.session.commit()
        await self.session.refresh(db_notification)

        return Notification.model_validate(db_notification)

    async def exists(self, task_id: UUID) -> bool:
        query = select(NotificationModel).where(NotificationModel.task_id == task_id)
        result = await self.session.execute(query)

        notification = result.scalar_one_or_none()

        return bool(notification)
