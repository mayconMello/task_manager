from typing import List

from app.domain.entities.category import Category
from app.infra.repositories.category_repository import CategoryRepository
from app.infra.repositories.user_repository import UserRepository


class ListCategoriesUseCase:
    def __init__(
        self,
        repository: CategoryRepository,
        repository_user=UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(self) -> List[Category]:
        categories = await self.repository.list()

        return categories
