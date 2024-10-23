from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.notifications.send_due_task_notification import (
    SendDueTaskNotificationUseCase,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_notification_repository import (
    SQLAlchemyNotificationRepository,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from app.infra.services.email_service import EmailService


class NotificationFactory:
    @staticmethod
    def repositories(session):
        repository = SQLAlchemyNotificationRepository(session)
        repository_task = SQLAlchemyTaskRepository(session)
        return repository, repository_task

    def send_due_task_notification_use_case(
        self,
        session: AsyncSession,
    ) -> SendDueTaskNotificationUseCase:
        email_service = EmailService()
        return SendDueTaskNotificationUseCase(
            *self.repositories(session),
            email_service=email_service,
        )
