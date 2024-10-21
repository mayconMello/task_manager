import pytest
import pytest_asyncio
from httpx import AsyncClient, Cookies

from app.core.auth import get_password_hash
from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.utils.tests.make_user import make_user, OverrideUser


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
async def test_e2e_refresh_token(
        client: AsyncClient,
        user: User
):
    payload = {
        'email': user.email,
        'password': 'ABC123456',
    }

    auth_response = await client.post(
        '/api/v1/sessions/',
        json=payload,
    )

    refresh_token = auth_response.cookies["refresh_token"]
    client.cookies.set('refresh_token', refresh_token)
    response = await client.post(
        '/api/v1/sessions/refresh'
    )

    assert response.status_code == 200
    data = response.json()

    assert 'access_token' in data

    cookies = response.cookies
    assert 'refresh_token' in cookies
