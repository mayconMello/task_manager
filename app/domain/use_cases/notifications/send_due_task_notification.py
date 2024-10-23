from collections import defaultdict
from datetime import datetime, timedelta

from app.domain.entities.notification import Notification
from app.infra.repositories.notification_repository import NotificationRepository
from app.infra.repositories.task_repository import TaskRepository
from app.infra.services.email_service import EmailService


class SendDueTaskNotificationUseCase:
    def __init__(
        self,
        repository: NotificationRepository,
        repository_task: TaskRepository,
        email_service: EmailService,
    ):
        self.repository = repository
        self.repository_task = repository_task
        self.email_service = email_service

    async def execute(self):
        now = datetime.now()
        due_date_limit = now + timedelta(hours=24)

        tasks = await self.repository_task.list_due_soon(due_date_limit)

        tasks_by_user = defaultdict(list)
        for task in tasks:
            already_sent = await self.repository.exists(task.id)
            if already_sent:
                continue

            tasks_by_user[task.user.email].append(task)

        for email, user_tasks in tasks_by_user.items():
            await self.email_service.send_task_notification(
                to_email=email, tasks=user_tasks
            )

            for task in user_tasks:
                notification = Notification(
                    task_id=task.id, user_id=task.user_id, sent_at=now
                )
                await self.repository.create(notification)
