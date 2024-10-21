from app.domain.entities.user import User
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.user_repository import UserRepository


class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> User:
        user = await self.repository.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError()

        return user
