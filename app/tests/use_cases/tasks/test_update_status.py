import pytest
import pytest_asyncio

from app.domain.entities.task import TaskUpdate
from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.tasks.update_status import UpdateStatusTaskUseCase
from app.infra.repositories.in_memory.in_memory_subtask_repository import (
    InMemorySubtaskRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_subtask import make_subtask, OverrideSubtask
from app.utils.tests.make_task import make_task, OverrideTask
from app.utils.tests.make_user import make_user


@pytest.fixture
def repository():
    return InMemoryTaskRepository()


@pytest.fixture
def repository_user():
    return InMemoryUserRepository()


@pytest.fixture
def repository_subtask():
    return InMemorySubtaskRepository()


@pytest.fixture
def use_case(
    repository: InMemoryTaskRepository,
    repository_user: InMemoryUserRepository,
    repository_subtask: InMemorySubtaskRepository,
):
    return UpdateStatusTaskUseCase(repository, repository_user, repository_subtask)


@pytest_asyncio.fixture
async def user(repository_user: InMemoryUserRepository):
    user = await repository_user.create(make_user())

    return user


@pytest.mark.asyncio
async def test_update_status_task(
    repository: InMemoryTaskRepository, use_case: UpdateStatusTaskUseCase, user: User
):
    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
            )
        )
    )

    await use_case.execute(task.id, user.id, True)

    assert repository.items[0].is_completed


@pytest.mark.asyncio
async def test_update_task_status_with_invalid_task_id(
    repository: InMemoryTaskRepository, use_case: UpdateStatusTaskUseCase, user: User
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
        await use_case.execute("invalid-task-id", user.id, True)


@pytest.mark.asyncio
async def test_update_status_task_with_invalid_user_id(
    repository: InMemoryTaskRepository, use_case: UpdateStatusTaskUseCase, user: User
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
        await use_case.execute(task.id, "invalid-user-id", True)


@pytest.mark.asyncio
async def test_subtasks_update_after_update_task(
    repository: InMemoryTaskRepository,
    repository_subtask: InMemorySubtaskRepository,
    use_case: UpdateStatusTaskUseCase,
    user: User,
):
    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
            )
        )
    )

    await repository_subtask.create(make_subtask(OverrideSubtask(task_id=task.id)))
    await repository_subtask.create(make_subtask(OverrideSubtask(task_id=task.id)))

    await use_case.execute(task.id, user.id, True)

    assert repository.items[0].is_completed

    for subtask in repository_subtask.items:
        assert subtask.is_completed
