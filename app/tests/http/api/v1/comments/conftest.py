import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.utils.tests.make_task import make_task, OverrideTask


@pytest_asyncio.fixture
async def task(
        session: AsyncSession,
        category: Category,
        user: User
) -> Task:
    repository = SQLAlchemyTaskRepository(
        session
    )

    task = await repository.create(
        make_task(
            OverrideTask(
                user_id=user.id,
                category_id=category.id
            )
        )
    )
    return task