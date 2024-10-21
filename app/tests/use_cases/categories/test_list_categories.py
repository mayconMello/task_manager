import pytest
from app.domain.use_cases.categories.list import ListCategoriesUseCase

from app.domain.entities.category import Category
from app.infra.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository


@pytest.fixture
def repository():
    return InMemoryCategoryRepository()


@pytest.fixture
def use_case(repository: InMemoryCategoryRepository):
    return ListCategoriesUseCase(repository)


@pytest.mark.asyncio
async def test_list_categories(
        use_case: ListCategoriesUseCase,
        repository: InMemoryCategoryRepository
):
    category_1 = Category(name='Category 1')
    category_2 = Category(name='Category 2')

    await repository.create(category_1)
    await repository.create(category_2)

    items = await use_case.execute()

    assert len(items) == 2

    assert items == repository.items
    assert items[0].name == 'Category 1'
    assert items[1].name == 'Category 2'
