import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.infra.db.models import UserModel


@pytest_asyncio.fixture
async def change_role_user(session: AsyncSession, user: User):
    query = select(UserModel).where(UserModel.id == user.id)
    result = await session.execute(query)
    user_db = result.scalar()

    user_db.role = "ADMIN"
    await session.commit()


@pytest.mark.asyncio
async def test_e2_create_category(
    client: AsyncClient,
    change_role_user,
    bearer_token: str,
):
    payload = {
        "name": "Test Category",
    }

    response = await client.post(
        "/api/v1/categories/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]


@pytest.mark.asyncio
async def test_e2_create_category_with_member(
    client: AsyncClient,
    bearer_token: str,
):
    payload = {
        "name": "Test Category",
    }

    response = await client.post(
        "/api/v1/categories/",
        json=payload,
        headers={"Authorization": f"Bearer {bearer_token}"},
    )

    assert response.status_code == 401
