import pytest
from httpx import AsyncClient
from starlette import status

from app.domain.entities.task import Task


@pytest.mark.asyncio
async def test_e2e_create_comment(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
):
    response = await client.post(
        f"/api/v1/tasks/{str(task.id)}/comments",
        headers={
            "Authorization": f"Bearer {bearer_token}",
        },
        json={"content": "Test add new comment"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    data["task_id"] = str(task.id)
    data["title"] = "Test title"


@pytest.mark.asyncio
async def test_e2e_create_comment_without_authentication(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
):
    response = await client.post(
        f"/api/v1/tasks/{str(task.id)}/comments",
        json={"title": "Test add new comment"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
