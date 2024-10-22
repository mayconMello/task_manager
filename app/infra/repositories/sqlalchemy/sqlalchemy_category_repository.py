from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.infra.db.models import CategoryModel
from app.infra.repositories.category_repository import CategoryRepository


class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        db_category = CategoryModel(
            name=category.name,
        )

        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)

        return Category.model_validate(db_category)

    async def list(self) -> List[Category]:
        result = await self.session.execute(select(CategoryModel))

        categories = result.scalars().all()

        categories = list(map(Category.model_validate, categories))

        return categories
