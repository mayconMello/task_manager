from datetime import datetime, timedelta

import pytest
import pytest_asyncio

from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.tasks.list_due_soon import ListTasksDueSoonUseCase
from app.infra.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from app.infra.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository
from app.utils.tests.make_task import make_task, OverrideTask
from app.utils.tests.make_user import make_user


@pytest.fixture
def repository():
    return InMemoryTaskRepository()


@pytest.fixture
def repository_user():
    return InMemoryUserRepository()


@pytest.fixture
def use_case(
        repository: InMemoryTaskRepository,
        repository_user: InMemoryUserRepository,
):
    return ListTasksDueSoonUseCase(
        repository,
        repository_user
    )


@pytest_asyncio.fixture
async def user(repository_user: InMemoryUserRepository):
    user = await repository_user.create(make_user())

    return user


@pytest.mark.asyncio
async def test_create_task(
        repository: InMemoryTaskRepository,
        use_case: ListTasksDueSoonUseCase,
        user: User
):
    task_due_soon = await repository.create(make_task(
        OverrideTask(
            title="Task Due Soon",
            due_date=datetime.now() + timedelta(hours=12),
            user_id=user.id,
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            title="Task Not Due Soon",
            due_date=datetime.now() + timedelta(days=2),
            user_id=user.id,
        )
    ))
    await repository.create(make_task())

    items = await use_case.execute(user.id)

    assert len(items) == 1
    assert items[0].id == task_due_soon.id


@pytest.mark.asyncio
async def test_create_task_with_invalid_user(
        repository: InMemoryTaskRepository,
        use_case: ListTasksDueSoonUseCase,
):
    await repository.create(make_task())

    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            'invalid-user-id'
        )
