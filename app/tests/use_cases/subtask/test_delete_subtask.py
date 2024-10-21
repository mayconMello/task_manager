import pytest
import pytest_asyncio

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.subtasks.delete import DeleteSubtaskUseCase
from app.infra.repositories.in_memory.in_memory_subtask_repository import InMemorySubtaskRepository
from app.infra.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
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
    return DeleteSubtaskUseCase(
        repository,
        repository_task
    )


@pytest_asyncio.fixture
async def task(
        repository_task: InMemoryTaskRepository,
):
    task = await repository_task.create(
        make_task()
    )

    return task


@pytest.mark.asyncio
async def test_delete_subtask(
        repository: InMemorySubtaskRepository,
        use_case: DeleteSubtaskUseCase,
        task
):
    subtask = await repository.create(
        make_subtask(
            OverrideSubtask(
                task_id=task.id,
            )
        )
    )
    await use_case.execute(
        task.user_id,
        task.id,
        subtask.id
    )

    assert len(repository.items) == 0


@pytest.mark.asyncio
async def test_delete_subtask_with_invalid_task_id(
        repository: InMemorySubtaskRepository,
        use_case: DeleteSubtaskUseCase,
        task
):
    subtask = await repository.create(
        make_subtask()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            'invalid-task-id',
            subtask.id
        )

    assert len(repository.items) == 1


@pytest.mark.asyncio
async def test_delete_subtask_with_invalid_id(
        repository: InMemorySubtaskRepository,
        use_case: DeleteSubtaskUseCase,
        task
):
    await repository.create(
        make_subtask()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            task.id,
            'invalid-subtask-id'
        )

    assert len(repository.items) == 1
