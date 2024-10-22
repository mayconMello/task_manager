import pytest
import pytest_asyncio

from app.domain.entities.task import TaskUpdate
from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.tasks.update import UpdateTaskUseCase
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


@pytest.fixture
def use_case(
    repository: InMemoryTaskRepository,
    repository_user: InMemoryUserRepository,
):
    return UpdateTaskUseCase(repository, repository_user)


@pytest_asyncio.fixture
async def user(repository_user: InMemoryUserRepository):
    user = await repository_user.create(make_user())

    return user


@pytest.mark.asyncio
async def test_update_task(repository: InMemoryTaskRepository, use_case: UpdateTaskUseCase, user: User):
    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
            )
        )
    )

    update = TaskUpdate.model_validate(task)
    update.title = "Updated title"

    await use_case.execute(task.id, user.id, update)

    assert repository.items[0].title == "Updated title"


@pytest.mark.asyncio
async def test_update_task_with_invalid_task_id(
    repository: InMemoryTaskRepository, use_case: UpdateTaskUseCase, user: User
):
    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
            )
        )
    )

    update = TaskUpdate.model_validate(task)
    update.title = "Updated title"

    with pytest.raises(ResourceNotFoundError):
        await use_case.execute("invalid-task-id", user.id, update)


@pytest.mark.asyncio
async def test_update_task_with_invalid_user_id(
    repository: InMemoryTaskRepository, use_case: UpdateTaskUseCase, user: User
):
    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
            )
        )
    )

    update = TaskUpdate.model_validate(task)
    update.title = "Updated title"

    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(task.id, "invalid-user-id", update)
