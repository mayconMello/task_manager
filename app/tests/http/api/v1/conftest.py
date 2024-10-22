import logging

import pytest_asyncio
from alembic.command import upgrade, downgrade
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash
from app.core.configs import settings
from app.domain.entities.category import Category
from app.infra.db.session import Session
from app.infra.repositories.sqlalchemy.sqlalchemy_category_repository import (
    SQLAlchemyCategoryRepository,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.main import app
from app.utils.tests.make_user import make_user, OverrideUser

logging.disable(logging.WARNING)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db_tear_down():
    if settings.environment != "test":
        raise RuntimeError("Environment not set to 'test'")

    config = Config("alembic.ini")
    upgrade(config, "head")

    yield

    downgrade(config, "base")


@pytest_asyncio.fixture(autouse=True, scope="function")
async def client(setup_db_tear_down):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture
async def session():
    async with Session() as session:
        yield session


@pytest_asyncio.fixture
async def category(session: AsyncSession):
    repository = SQLAlchemyCategoryRepository(session)

    category = await repository.create(Category(name="Test Category"))
    return category


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    repository = SQLAlchemyUserRepository(session)
    user = make_user(OverrideUser(password="ABC123456"))
    user.password = get_password_hash(user.password)
    user = await repository.create(user)

    return user


@pytest_asyncio.fixture
async def bearer_token(client: AsyncClient, user):
    response = await client.post("/api/v1/sessions/", json={"email": user.email, "password": "ABC123456"})

    data = response.json()
    token = data["access_token"]

    return token
