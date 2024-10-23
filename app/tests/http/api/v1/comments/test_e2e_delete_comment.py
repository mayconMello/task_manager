from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.comment import Comment
from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)
from app.utils.tests.make_comment import make_comment, OverrideComment


@pytest_asyncio.fixture
async def comment(session: AsyncSession, task: Task) -> Comment:
    repository = SQLAlchemyCommentRepository(session)

    comment = await repository.create(
        make_comment(
            OverrideComment(
                task_id=task.id.__str__(),
                user_id=task.user_id.__str__(),
            )
        )
    )
    return comment


@pytest.mark.asyncio
async def test_e2e_delete_comment(
    client: AsyncClient,
    bearer_token: str,
    task: Task,
    comment: Comment,
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id.__str__()}/comments/{comment.id.__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_e2e_delete_comment_without_authentication(
    client: AsyncClient,
    task: Task,
    comment: Comment,
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id.__str__()}/comments/{comment.id.__str__()}",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_delete_comment_with_invalid_id(
    client: AsyncClient, bearer_token: str, task: Task
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id}/comments/{uuid4().__str__()}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 400
