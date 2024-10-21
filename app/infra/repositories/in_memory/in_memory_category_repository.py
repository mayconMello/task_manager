import uuid
from typing import List

from app.domain.entities.category import Category
from app.infra.repositories.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):

    def __init__(self):
        self.items: List[Category] = []

    async def create(self, category: Category) -> Category:
        category.id = uuid.uuid4()
        self.items.append(category)

        return category

    async def list(self) -> List[Category]:
        return self.items
