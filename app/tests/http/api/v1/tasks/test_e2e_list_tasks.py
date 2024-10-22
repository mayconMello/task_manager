import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from app.utils.tests.make_task import make_task, OverrideTask


@pytest_asyncio.fixture
async def tasks(session: AsyncSession, category: Category, user: User):
    repository = SQLAlchemyTaskRepository(session)

    await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id,
                title="Buy groceries",
                description="Buy milk, eggs, and bread",
                priority="high",
            )
        )
    )
    await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id,
                title="Clean the house",
                description="Vacuum and dust",
                priority="medium",
            )
        )
    )
    await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id,
                title="Go for a run",
                description="Jog around the park",
                priority="low",
            )
        )
    )


@pytest.mark.asyncio
async def test_e2e_list_tasks(client: AsyncClient, bearer_token: str, tasks):
    response = await client.get("/api/v1/tasks/", headers={"Authorization": f"Bearer {bearer_token}"})

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3


@pytest.mark.asyncio
async def test_e2e_list_tasks_without_authentication(
    client: AsyncClient,
):
    response = await client.get("/api/v1/tasks/")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_list_tasks_by_title(client: AsyncClient, bearer_token: str, tasks):
    response = await client.get(
        "/api/v1/tasks/",
        params={"title": "groceries"},
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Buy groceries"


@pytest.mark.asyncio
async def test_e2e_list_tasks_by_description(client: AsyncClient, bearer_token: str, tasks):
    response = await client.get(
        "/api/v1/tasks/",
        params={"description": "Vacuum"},
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["description"] == "Vacuum and dust"


@pytest.mark.asyncio
async def test_e2e_list_tasks_by_priority(client: AsyncClient, bearer_token: str, tasks):
    response = await client.get(
        "/api/v1/tasks/",
        params={"priority": "high"},
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Buy groceries"
