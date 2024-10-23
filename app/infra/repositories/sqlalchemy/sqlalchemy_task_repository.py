from datetime import datetime
from typing import List, Optional

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.task import Task, TaskUpdate, TaskCreate
from app.infra.db.models import TaskModel
from app.infra.repositories.task_repository import TaskRepository


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskCreate) -> Task:
        task_db = TaskModel(
            **task.model_dump(exclude_none=True),
        )
        self.session.add(task_db)
        await self.session.commit()
        await self.session.refresh(task_db, ['category', 'user'])

        return Task.model_validate(task_db)

    async def list(self, user_id: UUID4, params: dict) -> List[Task]:
        query = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .options(selectinload(TaskModel.user))
            .options(selectinload(TaskModel.category))
        )
        if "title" in params:
            query = query.where(TaskModel.title.contains(params["title"]))
        if "description" in params:
            query = query.where(TaskModel.description.contains(params["description"]))
        if "priority" in params:
            query = query.where(TaskModel.priority == params["priority"])
        if "category_id" in params:
            query = query.where(TaskModel.category_id == params["category_id"])

        result = await self.session.execute(query)
        tasks = result.scalars().all()

        tasks = list(map(Task.model_validate, tasks))
        return tasks

    async def list_due_soon(
        self, due_time_limit: datetime, user_id: Optional[UUID4] = None
    ) -> List[Task]:
        query = (
            select(TaskModel)
            .options(selectinload(TaskModel.user))
            .options(selectinload(TaskModel.category))
            .where(
                TaskModel.due_date >= datetime.now(),
                TaskModel.due_date <= due_time_limit,
                TaskModel.is_completed.is_(False),
            )
        )
        if user_id:
            query = query.where(TaskModel.user_id == user_id)

        result = await self.session.execute(query)
        tasks = result.scalars().all()

        tasks = list(map(Task.model_validate, tasks))
        return tasks

    async def get(self, user_id: UUID4, task_id: UUID4) -> Task | None:
        query = (
            select(TaskModel)
            .options(selectinload(TaskModel.user))
            .options(selectinload(TaskModel.category))
            .where(TaskModel.id == task_id, TaskModel.user_id == user_id)
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return None

        return Task.model_validate(task)

    async def delete(self, task_id: UUID4) -> bool:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def update(self, task_id: UUID4, task: TaskUpdate) -> Task:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        db_task = result.scalar()

        for key, value in task.model_dump().items():
            setattr(db_task, key, value)

        await self.session.commit()
        await self.session.refresh(db_task, ['category', 'user'])
        return Task.model_validate(db_task)

    async def update_status(self, task_id: UUID4, is_completed: bool) -> Task:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar()
        task.is_completed = is_completed
        await self.session.commit()
        await self.session.refresh(task, ['category', 'user'])

        return Task.model_validate(task)
