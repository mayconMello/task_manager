import pytest
import pytest_asyncio

from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.tasks.list import ListTasksUseCase, TaskListFilter
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
    return ListTasksUseCase(
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
        use_case: ListTasksUseCase,
        user: User
):
    task_1 = await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))
    await repository.create(make_task())

    items = await use_case.execute(user.id)

    assert len(items) == 1
    assert items[0].id == task_1.id


@pytest.mark.asyncio
async def test_create_task_with_invalid_user(
        repository: InMemoryTaskRepository,
        use_case: ListTasksUseCase,
):
    await repository.create(make_task())

    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            'invalid-user-id'
        )


@pytest.mark.asyncio
async def test_filter_tasks_by_title(
        repository: InMemoryTaskRepository,
        use_case: ListTasksUseCase,
        user: User
):
    await repository.create(
        make_task(
            OverrideTask(
                title='Filter Task',
                user_id=user.id
            )
        )
    )
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))

    tasks = await use_case.execute(
        user.id,
        TaskListFilter(
            title="Filter"
        )
    )
    assert len(tasks) == 1
    assert tasks[0].title == "Filter Task"


@pytest.mark.asyncio
async def test_filter_tasks_by_description(
        repository: InMemoryTaskRepository,
        use_case: ListTasksUseCase,
        user: User
):
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            description='Filter Task by description',
            user_id=user.id
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))

    tasks = await use_case.execute(
        user.id,
        TaskListFilter(
            description="description"
        )
    )

    assert len(tasks) == 1
    assert tasks[0].description == "Filter Task by description"


@pytest.mark.asyncio
async def test_filter_tasks_by_priority(
        repository: InMemoryTaskRepository,
        use_case: ListTasksUseCase,
        user: User
):
    await repository.create(make_task(
        OverrideTask(
            priority='medium',
            user_id=user.id,
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            priority='medium',
            user_id=user.id,
        )
    ))
    task = await repository.create(make_task(
        OverrideTask(
            priority='high',
            user_id=user.id
        )
    ))

    tasks = await use_case.execute(
        user.id,
        TaskListFilter(
            priority="high"
        )
    )

    assert len(tasks) == 1
    assert tasks[0].title == task.title


@pytest.mark.asyncio
async def test_filter_tasks_by_category_id(
        repository: InMemoryTaskRepository,
        use_case: ListTasksUseCase,
        user: User
):
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))
    await repository.create(make_task(
        OverrideTask(
            user_id=user.id,
        )
    ))
    task = await repository.create(make_task(
        OverrideTask(
            user_id=user.id
        )
    ))

    tasks = await use_case.execute(
        user.id,
        TaskListFilter(
            category_id=task.category_id
        )
    )

    assert len(tasks) == 1
    assert tasks[0].title == task.title