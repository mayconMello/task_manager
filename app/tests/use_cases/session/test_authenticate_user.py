import pytest

from app.domain.entities.authenticate import Authenticate
from app.domain.errors import InvalidCredentialsError
from app.domain.use_cases.session.authenticate import AuthenticateUseCase
from app.domain.use_cases.users.create import CreateUserUseCase
from app.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from app.utils.tests.make_user import make_user, OverrideUser


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repository: InMemoryUserRepository):
    return AuthenticateUseCase(repository)


@pytest.mark.asyncio
async def test_authenticate_user(
    use_case: AuthenticateUseCase, repository: InMemoryUserRepository
):
    use_case_create_user = CreateUserUseCase(repository)

    user = make_user(OverrideUser(password="ABC123456"))
    await use_case_create_user.execute(user)

    authenticated_user = await use_case.execute(
        Authenticate(email=user.email, password="ABC123456")
    )

    assert authenticated_user.email == user.email


@pytest.mark.asyncio
async def test_authenticate_user_invalid_user(use_case: AuthenticateUseCase):
    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            Authenticate(email="jhondoe@example.com", password="ABC123456")
        )


@pytest.mark.asyncio
async def test_authenticate_with_invalid_password(
    use_case: AuthenticateUseCase, repository: InMemoryUserRepository
):
    use_case_create_user = CreateUserUseCase(repository)

    user = make_user(OverrideUser(password="ABC123456"))
    await use_case_create_user.execute(user)

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            Authenticate(email=user.email, password="invalid-password")
        )
