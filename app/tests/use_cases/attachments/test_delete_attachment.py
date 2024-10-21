import os

import pytest
import pytest_asyncio

from app.core.configs import settings, BASE_DIR
from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.attachments.delete import DeleteAttachmentUseCase
from app.infra.repositories.in_memory.in_memory_attachment_repository import InMemoryAttachmentRepository
from app.infra.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from app.utils.tests.make_attachment import make_attachment, OverrideAttachment
from app.utils.tests.make_task import make_task


@pytest.fixture
def test_storage_path():
    original_storage_path = settings.storage_full_path
    test_storage = BASE_DIR.joinpath('media/test_attachments')
    os.makedirs(test_storage, exist_ok=True)
    settings.storage_path = test_storage
    yield test_storage

    settings.storage_path = original_storage_path
    if test_storage.exists():
        for file in test_storage.iterdir():
            file.unlink()
        test_storage.rmdir()


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
    return DeleteAttachmentUseCase(
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
async def test_delete_attachment(
        repository: InMemoryAttachmentRepository,
        use_case: DeleteAttachmentUseCase,
        task,
        test_storage_path,
):
    filename = test_storage_path / 'test.txt'
    attachment = await repository.create(
        make_attachment(
            OverrideAttachment(
                task_id=task.id,
                filename='test.txt'
            )
        )
    )
    with open(filename, 'w') as file:
        file.write('test')

    await use_case.execute(
        task.user_id,
        task.id,
        attachment.id
    )

    assert len(repository.items) == 0
    assert not os.path.exists(filename)


@pytest.mark.asyncio
async def test_delete_attachment_with_invalid_task_id(
        repository: InMemoryAttachmentRepository,
        use_case: DeleteAttachmentUseCase,
        task
):
    attachment = await repository.create(
        make_attachment()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            'invalid-task-id',
            attachment.id
        )

    assert len(repository.items) == 1


@pytest.mark.asyncio
async def test_delete_attachment_with_invalid_id(
        repository: InMemoryAttachmentRepository,
        use_case: DeleteAttachmentUseCase,
        task
):
    await repository.create(
        make_attachment()
    )
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(
            task.user_id,
            task.id,
            'invalid-attachment-id'
        )

    assert len(repository.items) == 1
