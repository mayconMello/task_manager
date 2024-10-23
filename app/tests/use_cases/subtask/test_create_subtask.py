import pytest
import pytest_asyncio
from pydantic import ValidationError

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.subtasks.create import CreateSubtaskUseCase
from app.infra.repositories.in_memory.in_memory_subtask_repository import (
    InMemorySubtaskRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.utils.tests.make_subtask import make_subtask, OverrideSubtask
from app.utils.tests.make_task import make_task


@pytest.fixture
def repository():
    return InMemorySubtaskRepository()


@pytest.fixture
def repository_task():
    return InMemoryTaskRepository()


@pytest.fixture
def use_case(
    repository: InMemorySubtaskRepository,
    repository_task: InMemoryTaskRepository,
):
    return CreateSubtaskUseCase(repository, repository_task)


@pytest_asyncio.fixture
async def task(
    repository_task: InMemoryTaskRepository,
):
    task = await repository_task.create(make_task())

    return task


@pytest.mark.asyncio
async def test_create_subtask(
    repository: InMemorySubtaskRepository, use_case: CreateSubtaskUseCase, task
):
    subtask = await use_case.execute(
        task.user_id,
        task.id,
        make_subtask(
            OverrideSubtask(
                task_id=task.id,
            )
        ),
    )

    assert len(repository.items) == 1
    assert repository.items[0].title == subtask.title


@pytest.mark.asyncio
async def test_create_subtask_with_invalid_task_id(
    repository: InMemorySubtaskRepository, use_case: CreateSubtaskUseCase, task
):
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(task.user_id, "invalid-task_id", make_subtask())

    assert len(repository.items) == 0


@pytest.mark.asyncio
async def test_create_subtask_with_invalid_title(
    repository: InMemorySubtaskRepository, use_case: CreateSubtaskUseCase, task
):
    with pytest.raises(ValidationError):
        await use_case.execute(
            task.user_id,
            task.id,
            make_subtask(
                OverrideSubtask(
                    title="A" * 101,
                    task_id=task.id,
                )
            ),
        )

    assert len(repository.items) == 0
