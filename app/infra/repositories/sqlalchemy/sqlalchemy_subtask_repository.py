from typing import List

from pydantic import UUID4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.subtask import Subtask, SubtaskUpdate
from app.infra.db.models import SubtaskModel
from app.infra.repositories.subtask_repository import SubtaskRepository


class SQLAlchemySubtaskRepository(SubtaskRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subtask: Subtask) -> Subtask:
        db_subtask = SubtaskModel(
            title=subtask.title,
            is_completed=subtask.is_completed,
            task_id=subtask.task_id
        )
        self.session.add(db_subtask)
        await self.session.commit()
        await self.session.refresh(db_subtask)

        return Subtask.model_validate(db_subtask)

    async def update_all_status(
            self,
            task_id: UUID4,
            is_completed: bool
    ):
        await self.session.execute(
            update(SubtaskModel).where(
                SubtaskModel.task_id == task_id
            ).values(is_completed=is_completed)
        )
        await self.session.commit()

    async def update(
            self,
            task_id: UUID4,
            subtask_id: UUID4,
            subtask: SubtaskUpdate
    ) -> Subtask:
        result = await self.session.execute(
            select(SubtaskModel)
            .where(SubtaskModel.id == subtask_id)
            .where(SubtaskModel.task_id == task_id)
        )
        db_task = result.scalar()

        for key, value in subtask.model_dump().items():
            setattr(db_task, key, value)

        await self.session.commit()
        return Subtask.model_validate(db_task)

    async def delete(
            self,
            task_id: UUID4,
            subtask_id: UUID4
    ):
        query = (
            select(SubtaskModel)
            .where(SubtaskModel.id == subtask_id)
            .where(SubtaskModel.task_id == task_id)
        )
        result = await self.session.execute(query)

        subtask = result.scalar()

        await self.session.delete(subtask)
        await self.session.commit()

    async def get(self, task_id: UUID4, subtask_id: UUID4) -> Subtask | None:
        query = (
            select(SubtaskModel)
            .where(SubtaskModel.id == subtask_id)
            .where(SubtaskModel.task_id == task_id)
        )
        result = await self.session.execute(query)

        task = result.scalar_one_or_none()
        if task:
            return Subtask.model_validate(task)

        return task

    async def list(self, task_id: UUID4) -> List[Subtask]:
        query = select(SubtaskModel).where(SubtaskModel.task_id == task_id)
        result = await self.session.execute(query)
        subtask = result.scalars().all()

        subtasks = list(map(Subtask.model_validate, subtask))
        return subtasks
