from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.subtasks.create import CreateSubtaskUseCase
from app.domain.use_cases.subtasks.delete import DeleteSubtaskUseCase
from app.domain.use_cases.subtasks.get import GetSubtaskUseCase
from app.domain.use_cases.subtasks.list import ListSubtaskUseCase
from app.domain.use_cases.subtasks.update import UpdateSubtaskUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_subtask_repository import (
    SQLAlchemySubtaskRepository,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)


class SubtaskFactory:
    @staticmethod
    def repositories(session: AsyncSession):
        repository = SQLAlchemySubtaskRepository(session)
        repository_task = SQLAlchemyTaskRepository(session)

        return repository, repository_task

    def create_subtask_use_case(
        self, session: AsyncSession = Depends(get_session)
    ) -> CreateSubtaskUseCase:
        return CreateSubtaskUseCase(*self.repositories(session))

    def list_subtasks_use_case(
        self, session: AsyncSession = Depends(get_session)
    ) -> ListSubtaskUseCase:
        return ListSubtaskUseCase(*self.repositories(session))

    def get_subtask_use_case(
        self, session: AsyncSession = Depends(get_session)
    ) -> GetSubtaskUseCase:
        return GetSubtaskUseCase(*self.repositories(session))

    def delete_subtask_use_case(
        self, session: AsyncSession = Depends(get_session)
    ) -> DeleteSubtaskUseCase:
        return DeleteSubtaskUseCase(*self.repositories(session))

    def update_subtask_use_case(self, session: AsyncSession = Depends(get_session)):
        return UpdateSubtaskUseCase(*self.repositories(session))
