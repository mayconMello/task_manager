import pytest
import pytest_asyncio

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.comments.create import CreateCommentUseCase
from app.infra.repositories.in_memory.in_memory_comment_repository import (
    InMemoryCommentRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.utils.tests.make_comment import make_comment, OverrideComment
from app.utils.tests.make_task import make_task


@pytest.fixture
def repository():
    return InMemoryCommentRepository()


@pytest.fixture
def repository_task():
    return InMemoryTaskRepository()


@pytest.fixture
def use_case(
    repository: InMemoryCommentRepository,
    repository_task: InMemoryTaskRepository,
):
    return CreateCommentUseCase(repository, repository_task)


@pytest_asyncio.fixture
async def task(
    repository_task: InMemoryTaskRepository,
):
    task = await repository_task.create(make_task())

    return task


@pytest.mark.asyncio
async def test_create_comment(
    repository: InMemoryCommentRepository, use_case: CreateCommentUseCase, task
):
    comment = await use_case.execute(
        task.user_id,
        task.id,
        make_comment(
            OverrideComment(
                task_id=task.id,
            )
        ),
    )

    assert len(repository.items) == 1
    assert repository.items[0].content == comment.content


@pytest.mark.asyncio
async def test_create_comment_with_invalid_task_id(
    repository: InMemoryCommentRepository, use_case: CreateCommentUseCase, task
):
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(task.user_id, "invalid-task-id", make_comment())

    assert len(repository.items) == 0
