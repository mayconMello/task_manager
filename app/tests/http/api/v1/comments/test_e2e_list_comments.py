from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from app.utils.tests.make_comment import make_comment, OverrideComment


@pytest_asyncio.fixture
async def comments(
        session: AsyncSession,
        task: Task
):
    repository = SQLAlchemyCommentRepository(
        session
    )

    await repository.create(
        make_comment(
            OverrideComment(
                task_id=task.id.__str__(),
                user_id=task.user_id.__str__(),
                content='Comment 1'
            )
        )
    )
    await repository.create(
        make_comment(
            OverrideComment(
                task_id=task.id.__str__(),
                user_id=task.user_id.__str__(),
                content='Comment 2'
            )
        )
    )


@pytest.mark.asyncio
async def test_e2e_list_comments(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
        comments,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/comments",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]['content'] == 'Comment 1'
    assert data[1]['content'] == 'Comment 2'


@pytest.mark.asyncio
async def test_e2e_list_comments_without_authentication(
        client: AsyncClient,
        task: Task,
        comments,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/comments",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_list_comment_with_invalid_id(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
        comments
):
    response = await client.get(
        f"/api/v1/tasks/{uuid4().__str__()}/comments",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 400
