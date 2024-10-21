import pytest
import pytest_asyncio

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.comments.delete import DeleteCommentUseCase
from app.infra.repositories.in_memory.in_memory_comment_repository import InMemoryCommentRepository
from app.infra.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
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
    return DeleteCommentUseCase(
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
async def test_delete_comment(
        repository: InMemoryCommentRepository,
        use_case: DeleteCommentUseCase,
        task
):
    comment = await repository.create(
        make_comment(
            OverrideComment(
                task_id=task.id,
            )
        )
    )
    await use_case.execute(
        task.user_id,
        task.id,
        comment.id
    )

    assert len(repository.items) == 0


@pytest.mark.asyncio
async def test_delete_comment_with_invalid_task_id(
        repository: InMemoryCommentRepository,
        use_case: DeleteCommentUseCase,
        task
):
    comment = await repository.create(
        make_comment()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            'invalid-task-id',
            comment.id
        )

    assert len(repository.items) == 1


@pytest.mark.asyncio
async def test_delete_comment_with_invalid_id(
        repository: InMemoryCommentRepository,
        use_case: DeleteCommentUseCase,
        task
):
    await repository.create(
        make_comment()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            task.id,
            'invalid-comment-id'
        )

    assert len(repository.items) == 1
