from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.categories.create import CreateCategoryUseCase
from app.domain.use_cases.categories.list import ListCategoriesUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_category_repository import SQLAlchemyCategoryRepository
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository


class CategoryFactory:

    @staticmethod
    def repositories(session: AsyncSession):
        repository = SQLAlchemyCategoryRepository(session)
        repository_user = SQLAlchemyUserRepository(session)
        return repository, repository_user

    def create_category_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> CreateCategoryUseCase:
        return CreateCategoryUseCase(*self.repositories(session))

    def list_categories_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> ListCategoriesUseCase:
        return ListCategoriesUseCase(*self.repositories(session))
