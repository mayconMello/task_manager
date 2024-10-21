from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_attachment_repository import SQLAlchemyAttachmentRepository
from app.utils.tests.make_attachment import make_attachment, OverrideAttachment


@pytest_asyncio.fixture
async def attachments(
        session: AsyncSession,
        task: Task
):
    repository = SQLAlchemyAttachmentRepository(
        session
    )

    await repository.create(
        make_attachment(
            OverrideAttachment(
                task_id=task.id.__str__(),
                original_name='teste_1.txt'
            )
        )
    )
    await repository.create(
        make_attachment(
            OverrideAttachment(
                task_id=task.id.__str__(),
                original_name='teste_2.txt'
            )
        )
    )


@pytest.mark.asyncio
async def test_e2e_list_attachments(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
        attachments,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/attachments",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]['original_name'] == 'teste_1.txt'
    assert data[1]['original_name'] == 'teste_2.txt'


@pytest.mark.asyncio
async def test_e2e_list_attachments_without_authentication(
        client: AsyncClient,
        task: Task,
        attachments,
):
    response = await client.get(
        f"/api/v1/tasks/{task.id.__str__()}/attachments",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_list_attachment_with_invalid_id(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
        attachments
):
    response = await client.get(
        f"/api/v1/tasks/{uuid4().__str__()}/attachments",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 400
