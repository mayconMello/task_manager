from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Category]:
        raise NotImplementedError
