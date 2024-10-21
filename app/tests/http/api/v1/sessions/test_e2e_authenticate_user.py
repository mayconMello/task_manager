import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.utils.tests.make_user import make_user, OverrideUser
from app.core.auth import get_password_hash


@pytest_asyncio.fixture
async def user(session):
    repository = SQLAlchemyUserRepository(session)
    user = make_user(
        OverrideUser(
            email='jhondoe@example.com',
            password=get_password_hash('ABC123456'),
        )
    )
    await repository.create(user)
    return user


@pytest.mark.asyncio
async def test_e2e_authenticate_user(
        client: AsyncClient,
        user: User
):
    payload = {
        'email': user.email,
        'password': 'ABC123456',
    }

    response = await client.post(
        '/api/v1/sessions/',
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()

    assert 'access_token' in data

    cookies = response.cookies
    assert 'refresh_token' in cookies


@pytest.mark.asyncio
async def test_e2e_authenticate_with_invalid_email(
        client: AsyncClient,
        user: User
):
    payload = {
        'email': 'invalid-email@example.com',
        'password': 'ABC123456',
    }

    response = await client.post(
        '/api/v1/sessions/',
        json=payload,
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_e2e_authenticate_with_invalid_password(
        client: AsyncClient,
        user: User
):
    payload = {
        'email': user.email,
        'password': 'invalid-password',
    }

    response = await client.post(
        '/api/v1/sessions/',
        json=payload,
    )

    assert response.status_code == 401