from app.core.auth import verify_password
from app.domain.entities.authenticate import Authenticate
from app.domain.entities.user import User
from app.domain.errors import InvalidCredentialsError
from app.infra.repositories.user_repository import UserRepository


class AuthenticateUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, body: Authenticate) -> User:
        user = await self.repository.get_by_email(body.email)

        if not user:
            raise InvalidCredentialsError()

        is_correct_password = verify_password(body.password, user.password)

        if not is_correct_password:
            raise InvalidCredentialsError()

        return user
