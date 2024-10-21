from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.utils.tests.make_task import make_task, OverrideTask


@pytest_asyncio.fixture
async def tasks(
        session: AsyncSession,
        category: Category,
        user: User
):
    repository = SQLAlchemyTaskRepository(
        session
    )

    due_soon = datetime.now() + timedelta(hours=12)
    not_due_soon = datetime.now() + timedelta(days=2)

    await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id,
                due_date=due_soon.isoformat(timespec='seconds'),
                title='Due Soon Task'
            )
        )
    )
    await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id,
                due_date=not_due_soon.isoformat(timespec='seconds'),
            )
        )
    )


@pytest.mark.asyncio
async def test_e2e_list_tasks_due_soon(
        client: AsyncClient,
        bearer_token: str,
        tasks
):
    response = await client.get(
        "/api/v1/tasks/due-soon",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1

    assert data[0]['title'] == 'Due Soon Task'


@pytest.mark.asyncio
async def test_e2e_list_tasks_due_soon_without_authentication(
        client: AsyncClient,
):
    response = await client.get(
        "/api/v1/tasks/due-soon"
    )

    assert response.status_code == 401
