from uuid import uuid4

import pytest
import pytest_asyncio

from app.domain.entities.category import Category
from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError, OperationNotAllowedError
from app.domain.use_cases.categories.create import CreateCategoryUseCase
from app.infra.repositories.in_memory.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_user import make_user, OverrideUser


@pytest.fixture
def repository():
    return InMemoryCategoryRepository()


@pytest.fixture
def repository_user():
    return InMemoryUserRepository()


@pytest_asyncio.fixture
async def user_not_allowed(repository_user: InMemoryUserRepository) -> User:
    user = await repository_user.create(make_user())
    return user


@pytest_asyncio.fixture
async def user(repository_user: InMemoryUserRepository) -> User:
    user = await repository_user.create(make_user(OverrideUser(role="ADMIN")))
    repository_user.items[0].role = "ADMIN"
    return user


@pytest.fixture
def use_case(repository: InMemoryCategoryRepository, repository_user: InMemoryUserRepository):
    return CreateCategoryUseCase(repository, repository_user)


@pytest.mark.asyncio
async def test_create_category(use_case: CreateCategoryUseCase, repository: InMemoryCategoryRepository, user: User):
    category = await use_case.execute(user.id, Category(name="Some Category"))

    assert len(repository.items) == 1
    assert category.name == "Some Category"
    assert repository.items[0].name == "Some Category"


@pytest.mark.asyncio
async def test_create_category_with_invalid_user_id(
    use_case: CreateCategoryUseCase, repository: InMemoryCategoryRepository, user: User
):
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute(uuid4().__str__(), Category(name="Some Category"))


@pytest.mark.asyncio
async def test_create_category_with_nonauthorized_user(
    use_case: CreateCategoryUseCase,
    repository: InMemoryCategoryRepository,
    user_not_allowed: User,
):
    with pytest.raises(OperationNotAllowedError):
        await use_case.execute(user_not_allowed.id, Category(name="Some Category"))
