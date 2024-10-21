from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.attachment import Attachment
from app.domain.entities.task import Task
from app.infra.repositories.sqlalchemy.sqlalchemy_attachment_repository import SQLAlchemyAttachmentRepository
from app.utils.tests.make_attachment import make_attachment, OverrideAttachment


@pytest_asyncio.fixture
async def attachment(
        session: AsyncSession,
        task: Task
) -> Attachment:
    repository = SQLAlchemyAttachmentRepository(
        session
    )

    attachment = await repository.create(
        make_attachment(
            OverrideAttachment(
                task_id=task.id.__str__(),
                user_id=task.user_id.__str__(),
            )
        )
    )
    return attachment


@pytest.mark.asyncio
async def test_e2e_delete_attachment(
        client: AsyncClient,
        bearer_token: str,
        task: Task,
        attachment: Attachment,
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id.__str__()}/attachments/{attachment.id.__str__()}",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_e2e_delete_attachment_without_authentication(
        client: AsyncClient,
        task: Task,
        attachment: Attachment,
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id.__str__()}/attachments/{attachment.id.__str__()}",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_delete_attachment_with_invalid_id(
        client: AsyncClient,
        bearer_token: str,
        task: Task
):
    response = await client.delete(
        f"/api/v1/tasks/{task.id}/attachments/{uuid4().__str__()}",
        headers={
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 400
