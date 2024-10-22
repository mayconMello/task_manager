from datetime import datetime

import pytest
import pytest_asyncio
from pydantic import ValidationError

from app.domain.entities.user import User
from app.domain.use_cases.tasks.create import CreateTaskUseCase
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_task import make_task, OverrideTask
from app.utils.tests.make_user import make_user


@pytest.fixture
def repository():
    return InMemoryTaskRepository()


@pytest.fixture
def repository_user():
    return InMemoryUserRepository()


@pytest_asyncio.fixture
async def user(repository_user: InMemoryUserRepository) -> User:
    user = await repository_user.create(make_user())
    return user


@pytest.fixture
def use_case(repository: InMemoryTaskRepository, repository_user: InMemoryUserRepository) -> CreateTaskUseCase:
    return CreateTaskUseCase(repository, repository_user)


@pytest.mark.asyncio
async def test_create_task(repository: InMemoryTaskRepository, use_case: CreateTaskUseCase, user: User):
    task = await use_case.execute(user.id, make_task())

    assert len(repository.items) == 1
    assert repository.items[0].title == task.title


@pytest.mark.asyncio
async def test_create_task_with_title_more_than_100_caracters(
    repository: InMemoryTaskRepository, use_case: CreateTaskUseCase, user: User
):
    with pytest.raises(ValidationError):
        await use_case.execute(
            user.id,
            make_task(
                OverrideTask(
                    title="A" * 101,
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_task_with_invalid_due_date(
    repository: InMemoryTaskRepository, use_case: CreateTaskUseCase, user: User
):
    with pytest.raises(ValidationError):
        await use_case.execute(user.id, make_task(OverrideTask(due_date=datetime.now())))
