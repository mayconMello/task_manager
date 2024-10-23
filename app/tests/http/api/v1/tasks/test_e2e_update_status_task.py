from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from app.utils.tests.make_task import make_task, OverrideTask


@pytest_asyncio.fixture
async def task(session: AsyncSession, category: Category, user: User) -> Task:
    repository = SQLAlchemyTaskRepository(session)

    task = await repository.create(
        make_task(OverrideTask(user_id=user.id, category_id=category.id))
    )
    return task


@pytest.mark.asyncio
async def test_e2e_update_status_task(
    client: AsyncClient, bearer_token: str, task: Task
):
    response = await client.patch(
        f"/api/v1/tasks/{task.id.__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"is_completed": True},
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert data["is_completed"]


@pytest.mark.asyncio
async def test_e2e_update_status_task_without_authentication(
    client: AsyncClient, task: Task
):
    response = await client.patch(
        f"/api/v1/tasks/{task.id.__str__()}", json={"is_completed": True}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_update_status_task_with_invalid_id(
    client: AsyncClient, bearer_token: str, task: Task
):
    response = await client.patch(
        f"/api/v1/tasks/{uuid4().__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json={"is_completed": True},
    )

    assert response.status_code == 400
