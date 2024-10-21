from pydantic.v1 import UUID4

from app.domain.entities.category import Category
from app.domain.errors import ResourceNotFoundError, OperationNotAllowedError
from app.infra.repositories.category_repository import CategoryRepository
from app.infra.repositories.user_repository import UserRepository


class CreateCategoryUseCase:
    def __init__(
            self,
            repository: CategoryRepository,
            repository_user: UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(self, user_id: str, body: Category) -> Category:
        user = await self.repository_user.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError()

        if user.role != 'ADMIN':
            raise OperationNotAllowedError()

        category = await self.repository.create(body)

        return category
