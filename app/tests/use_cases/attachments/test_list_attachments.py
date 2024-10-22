import pytest
import pytest_asyncio

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.attachments.list import ListAttachmentsUseCase
from app.infra.repositories.in_memory.in_memory_attachment_repository import (
    InMemoryAttachmentRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
from app.utils.tests.make_attachment import make_attachment, OverrideAttachment
from app.utils.tests.make_task import make_task


@pytest.fixture
def repository():
    return InMemoryAttachmentRepository()


@pytest.fixture
def repository_task():
    return InMemoryTaskRepository()


@pytest.fixture
def use_case(
    repository: InMemoryAttachmentRepository,
    repository_task: InMemoryTaskRepository,
):
    return ListAttachmentsUseCase(repository, repository_task)


@pytest_asyncio.fixture
async def task(
    repository_task: InMemoryTaskRepository,
):
    task = await repository_task.create(make_task())

    return task


@pytest.mark.asyncio
async def test_list_attachments(repository: InMemoryAttachmentRepository, use_case: ListAttachmentsUseCase, task):
    attachment = await repository.create(
        make_attachment(
            OverrideAttachment(
                task_id=task.id,
            )
        )
    )
    await repository.create(make_attachment())

    attachments = await use_case.execute(
        task.user_id,
        task.id,
    )

    assert len(attachments) == 1
    assert attachments[0].filename == attachment.filename


@pytest.mark.asyncio
async def test_list_attachments_with_invalid_task_id(
    repository: InMemoryAttachmentRepository, use_case: ListAttachmentsUseCase, task
):
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(task.user_id, "invalid-task-id")

    assert len(repository.items) == 0
