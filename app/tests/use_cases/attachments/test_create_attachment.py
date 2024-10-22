import os
from io import BytesIO

import pytest
import pytest_asyncio
from fastapi import UploadFile

from app.core.configs import settings, BASE_DIR
from app.domain.errors import ResourceNotFoundError, MaxFileSizeError
from app.domain.use_cases.attachments.create import CreateAttachmentUseCase
from app.infra.repositories.in_memory.in_memory_attachment_repository import (
    InMemoryAttachmentRepository,
)
from app.infra.repositories.in_memory.in_memory_task_repository import (
    InMemoryTaskRepository,
)
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
    test_storage_path,
):
    return CreateAttachmentUseCase(repository, repository_task, test_storage_path)


@pytest_asyncio.fixture
async def task(
    repository_task: InMemoryTaskRepository,
):
    task = await repository_task.create(make_task())

    return task


@pytest.fixture
def test_storage_path():
    original_storage_path = settings.storage_full_path
    test_storage = BASE_DIR.joinpath("media/test_attachments")
    os.makedirs(test_storage, exist_ok=True)
    settings.storage_path = test_storage
    yield test_storage

    settings.storage_path = original_storage_path
    if test_storage.exists():
        for file in test_storage.iterdir():
            file.unlink()
        test_storage.rmdir()


@pytest.mark.asyncio
async def test_create_attachment(
    repository: InMemoryAttachmentRepository,
    use_case: CreateAttachmentUseCase,
    task,
    test_storage_path,
):
    file_content = b"Test content"
    file = UploadFile(filename="test_file.txt", file=BytesIO(file_content), size=1)

    attachment = await use_case.execute(task.user_id, task.id, file)

    expected_file_path = test_storage_path / attachment.filename
    assert expected_file_path.exists()

    with open(expected_file_path, "rb") as f:
        content = f.read()
        assert content == file_content

    expected_file_path.unlink()


@pytest.mark.asyncio
async def test_create_attachment_with_invalid_task_id(
    repository: InMemoryAttachmentRepository, use_case: CreateAttachmentUseCase, task
):
    file = UploadFile(filename="test_file.txt", file=BytesIO(b"Test content"), size=1)

    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(task.user_id, "invalid-task-id", file)

    assert len(repository.items) == 0


@pytest.mark.asyncio
async def test_create_attachment_with_large_file(
    repository: InMemoryAttachmentRepository,
    use_case: CreateAttachmentUseCase,
    task,
    test_storage_path,
):
    large_file_content = b"A" * (settings.max_file_size_bytes + 1)
    file = UploadFile(
        filename="large_test_file.txt",
        file=BytesIO(large_file_content),
        size=settings.max_file_size_bytes + 1,
    )

    with pytest.raises(MaxFileSizeError):
        await use_case.execute(task.user_id, task.id, file)
