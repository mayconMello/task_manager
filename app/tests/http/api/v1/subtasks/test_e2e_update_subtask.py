from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.subtask import Subtask
from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_subtask_repository import (
    SQLAlchemySubtaskRepository,
)
from app.utils.tests.make_subtask import make_subtask, OverrideSubtask


@pytest_asyncio.fixture
async def subtask(session: AsyncSession, task: Task) -> Subtask:
    repository = SQLAlchemySubtaskRepository(session)

    subtask = await repository.create(make_subtask(OverrideSubtask(task_id=task.id.__str__())))
    return subtask


@pytest.mark.asyncio
async def test_e2e_update_subtask(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
    subtask: Subtask,
):
    response = await client.put(
        f"/api/v1/tasks/{task.id.__str__()}/subtasks/{subtask.id.__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"title": "Updated title", "is_completed": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["is_completed"] is True


@pytest.mark.asyncio
async def test_e2e_update_subtask_without_authentication(
    client: AsyncClient,
    task: Task,
    subtask: Subtask,
):
    response = await client.put(
        f"/api/v1/tasks/{task.id.__str__()}/subtasks/{subtask.id.__str__()}",
        json={"title": "Updated title", "is_completed": True},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_update_subtask_with_invalid_id(client: AsyncClient, bearer_token: str, task: Task):
    response = await client.put(
        f"/api/v1/tasks/{task.id}/subtasks/{uuid4().__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"title": "Updated title", "is_completed": True},
    )

    assert response.status_code == 400
