import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.infra.repositories.sqlalchemy.sqlalchemy_category_repository import (
    SQLAlchemyCategoryRepository,
)


@pytest_asyncio.fixture
async def categories(session: AsyncSession):
    repository = SQLAlchemyCategoryRepository(session)

    await repository.create(Category(name="Category 1"))
    await repository.create(Category(name="Category 2"))
    await repository.create(Category(name="Category 3"))


@pytest.mark.asyncio
async def test_e2e_list_categories(
    categories,
    client: AsyncClient,
):
    response = await client.get(
        "/api/v1/categories/",
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
