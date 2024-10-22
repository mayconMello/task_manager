from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.tasks.create import CreateTaskUseCase
from app.domain.use_cases.tasks.delete import DeleteTaskUseCase
from app.domain.use_cases.tasks.get import GetTaskUseCase
from app.domain.use_cases.tasks.list import ListTasksUseCase
from app.domain.use_cases.tasks.list_due_soon import ListTasksDueSoonUseCase
from app.domain.use_cases.tasks.update import UpdateTaskUseCase
from app.domain.use_cases.tasks.update_status import UpdateStatusTaskUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_subtask_repository import (
    SQLAlchemySubtaskRepository,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


class TaskUseCaseFactory:
    @staticmethod
    def repositories(session: AsyncSession):
        repository_task = SQLAlchemyTaskRepository(session=session)
        repository_user = SQLAlchemyUserRepository(session=session)

        return repository_task, repository_user

    def create_task_use_case(self, session: AsyncSession = Depends(get_session)) -> CreateTaskUseCase:
        repositories = self.repositories(session=session)
        return CreateTaskUseCase(*repositories)

    def list_tasks_use_case(self, session: AsyncSession = Depends(get_session)) -> ListTasksUseCase:
        repositories = self.repositories(session=session)
        return ListTasksUseCase(*repositories)

    def list_tasks_due_soon_use_case(self, session: AsyncSession = Depends(get_session)) -> ListTasksDueSoonUseCase:
        repositories = self.repositories(session=session)
        return ListTasksDueSoonUseCase(*repositories)

    def get_task_use_case(self, session: AsyncSession = Depends(get_session)) -> GetTaskUseCase:
        repositories = self.repositories(session=session)
        return GetTaskUseCase(*repositories)

    def delete_task_use_case(self, session: AsyncSession = Depends(get_session)) -> DeleteTaskUseCase:
        repositories = self.repositories(session=session)
        return DeleteTaskUseCase(*repositories)

    def update_task_use_case(self, session: AsyncSession = Depends(get_session)) -> UpdateTaskUseCase:
        repositories = self.repositories(session)
        return UpdateTaskUseCase(*repositories)

    def update_status_task_use_case(self, session: AsyncSession = Depends(get_session)) -> UpdateStatusTaskUseCase:
        repositories = self.repositories(session)
        repository_subtask = SQLAlchemySubtaskRepository(session)
        return UpdateStatusTaskUseCase(*repositories, repository_subtask=repository_subtask)
