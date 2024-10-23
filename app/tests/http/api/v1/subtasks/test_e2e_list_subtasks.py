from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_subtask_repository import (
    SQLAlchemySubtaskRepository,
)
from app.utils.tests.make_subtask import make_subtask, OverrideSubtask


@pytest_asyncio.fixture
async def subtasks(session: AsyncSession, task: Task):
    repository = SQLAlchemySubtaskRepository(session)

    await repository.create(
        make_subtask(OverrideSubtask(task_id=task.id.__str__(), title="Subtask 1"))
    )
    await repository.create(
        make_subtask(OverrideSubtask(task_id=task.id.__str__(), title="Subtask 2"))
    )


@pytest.mark.asyncio
async def test_e2e_list_subtasks(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
    subtasks,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/subtasks",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Subtask 1"
    assert data[1]["title"] == "Subtask 2"


@pytest.mark.asyncio
async def test_e2e_list_subtasks_without_authentication(
    client: AsyncClient,
    task: Task,
    subtasks,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/subtasks",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_list_subtask_with_invalid_id(
    client: AsyncClient, bearer_token: str, task: Task, subtasks
):
    response = await client.get(
        f"/api/v1/tasks/{uuid4().__str__()}/subtasks",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 400
