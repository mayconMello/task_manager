import pytest

from app.core.auth import verify_password
from app.domain.errors import UserAlreadyExists
from app.domain.use_cases.users.create import CreateUserUseCase
from app.infra.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository
from app.utils.tests.make_user import make_user, OverrideUser


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repository: InMemoryUserRepository):
    return CreateUserUseCase(repository)


@pytest.mark.asyncio
async def test_create_user(
        repository: InMemoryUserRepository,
        use_case: CreateUserUseCase
):
    user = await use_case.execute(make_user())

    assert repository.items[0].email == user.email


@pytest.mark.asyncio
async def test_create_user_with_same_email_twice(
        repository: InMemoryUserRepository,
        use_case: CreateUserUseCase
):
    await repository.create(make_user(OverrideUser(
        email='jhondoe@example.com',
    )))

    with pytest.raises(UserAlreadyExists):
        await use_case.execute(make_user(OverrideUser(
            email='jhondoe@example.com',
        )))

    assert len(repository.items) == 1


@pytest.mark.asyncio
async def test_password_hash_on_create_user(
        repository: InMemoryUserRepository,
        use_case: CreateUserUseCase
):
    user = await use_case.execute(make_user(
        OverrideUser(
            password='ABC123456'
        )
    ))

    is_password_correctly_hash = verify_password(
        'ABC123456',
        user.password
    )

    assert is_password_correctly_hash is True
