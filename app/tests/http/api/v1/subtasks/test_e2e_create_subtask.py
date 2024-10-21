import pytest
from httpx import AsyncClient
from starlette import status

from app.domain.entities.task import Task


@pytest.mark.asyncio
async def test_e2e_create_subtask(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
):
    response = await client.post(
        f'/api/v1/tasks/{str(task.id)}/subtasks',
        headers={
            "Authorization": f"Bearer {bearer_token}",
        },
        json={
            'title': 'Test subtask title'
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    data['task_id'] = str(task.id)
    data['title'] = 'Test title'


@pytest.mark.asyncio
async def test_e2e_create_subtask_without_authentication(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
):
    response = await client.post(
        f'/api/v1/tasks/{str(task.id)}/subtasks',
        json={
            'title': 'Test subtask title'
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
