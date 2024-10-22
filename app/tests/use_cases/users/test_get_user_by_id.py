import pytest

from app.domain.errors import ResourceNotFoundError
from app.domain.use_cases.users.get_by_id import GetUserByIdUseCase
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_user import make_user


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repository: InMemoryUserRepository):
    return GetUserByIdUseCase(repository)


@pytest.mark.asyncio
async def test_get_user_by_id(use_case: GetUserByIdUseCase, repository: InMemoryUserRepository):
    created_user = await repository.create(make_user())

    user = await use_case.execute(created_user.id)

    assert user == created_user


@pytest.mark.asyncio
async def test_get_user_with_invalid_id(use_case: GetUserByIdUseCase, repository: InMemoryUserRepository):
    with pytest.raises(ResourceNotFoundError):
        await use_case.execute("invalid-id")
