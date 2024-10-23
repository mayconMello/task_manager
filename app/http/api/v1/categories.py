from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.core.auth import get_current_user
from app.domain.entities.category import Category
from app.domain.use_cases.categories.create import CreateCategoryUseCase
from app.domain.use_cases.categories.list import ListCategoriesUseCase
from app.infra.factories.category_factory import CategoryFactory

router = APIRouter(tags=["Categories"])

category_factory = CategoryFactory()


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create(
    body: Category,
    use_case: CreateCategoryUseCase = Depends(
        category_factory.create_category_use_case
    ),
    current_user: str = Depends(get_current_user),
):
    category = await use_case.execute(current_user, body)

    return category


@router.get("/", response_model=List[Category])
async def list_categories(
    use_case: ListCategoriesUseCase = Depends(
        category_factory.list_categories_use_case
    ),
):
    categories = await use_case.execute()

    return categories
