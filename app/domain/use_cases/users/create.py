from app.core.auth import get_password_hash
from app.domain.entities.user import User, UserCreate
from app.domain.errors import UserAlreadyExists
from app.infra.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, body: UserCreate) -> User:
        user_exists = await self.repository.get_by_email(body.email)

        if user_exists:
            raise UserAlreadyExists()

        body.password = get_password_hash(body.password)
        user = await self.repository.create(body)

        return user
