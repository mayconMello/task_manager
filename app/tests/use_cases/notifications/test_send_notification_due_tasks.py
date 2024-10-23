from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.domain.use_cases.notifications.send_due_task_notification import (
    SendDueTaskNotificationUseCase,
)
from app.infra.repositories.in_memory.in_memory_notification_repository import (
    InMemoryNotificationRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_task import make_task, OverrideTask
from app.utils.tests.make_user import make_user


@pytest.mark.asyncio
async def test_send_notification_only_for_due_tasks():
    repository = InMemoryNotificationRepository()
    repository_task = InMemoryTaskRepository()
    repository_user = InMemoryUserRepository()
    email_service_mock = AsyncMock()
    use_case = SendDueTaskNotificationUseCase(
        repository, repository_task, email_service_mock
    )

    user_1 = await repository_user.create(make_user())
    user_2 = await repository_user.create(make_user())

    task_1 = await repository_task.create(
        make_task(
            OverrideTask(
                title="Task Due Soon 1",
                due_date=datetime.now() + timedelta(hours=12),
                user_id=user_1.id,
            )
        )
    )
    repository_task.items[0].user = user_1
    task_2 = await repository_task.create(
        make_task(
            OverrideTask(
                title="Task Due Soon 2",
                due_date=datetime.now() + timedelta(hours=10),
                user_id=user_2.id,
                user=user_2,
            )
        )
    )
    repository_task.items[1].user = user_2
    await repository_task.create(
        make_task(
            OverrideTask(
                title="Task Not Due Soon", due_date=datetime.now() + timedelta(days=2)
            )
        )
    )

    await use_case.execute()

    assert email_service_mock.send_task_notification.call_count == 2

    email_service_mock.send_task_notification.assert_any_call(
        to_email=user_1.email, tasks=[task_1]
    )
    email_service_mock.send_task_notification.assert_any_call(
        to_email=user_2.email, tasks=[task_2]
    )

    assert repository.items[0].task_id == task_1.id
    assert repository.items[1].task_id == task_2.id
