import pytest
from httpx import AsyncClient
from starlette import status

from app.core.configs import settings
from app.domain.entities.task import Task


@pytest.mark.asyncio
async def test_e2e_create_attachment(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
    test_storage_path,
):
    file_path = test_storage_path.joinpath("test_upload.txt")
    file_content = b"Sample file content for testing."

    file_path.write_bytes(file_content)

    with open(file_path, "rb") as test_file:
        files = {"file": ("test_upload.txt", test_file, "text/plain")}
        response = await client.post(
            f"/api/v1/tasks/{str(task.id)}/attachments",
            headers={
                "Authorization": f"Bearer {bearer_token}",
            },
            files=files,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        data["task_id"] = str(task.id)
        data["original_name"] = "test_upload.txt"

    file_path.unlink()


@pytest.mark.asyncio
async def test_e2e_create_attachment_with_large_file(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
    test_storage_path,
):
    file_path = test_storage_path.joinpath("test_upload.txt")
    file_content = b"A" * (settings.MAX_FILE_SIZE_BYTES + 1)

    file_path.write_bytes(file_content)

    with open(file_path, "rb") as test_file:
        files = {"file": ("test_upload.txt", test_file, "text/plain")}
        response = await client.post(
            f"/api/v1/tasks/{str(task.id)}/attachments",
            headers={
                "Authorization": f"Bearer {bearer_token}",
            },
            files=files,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    file_path.unlink()


@pytest.mark.asyncio
async def test_e2e_create_attachment_without_authentication(
    client: AsyncClient, bearer_token: str, task: Task
):
    response = await client.post(f"/api/v1/tasks/{str(task.id)}/attachments", files={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
