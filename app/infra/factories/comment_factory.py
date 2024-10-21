from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.comments.create import CreateCommentUseCase
from app.domain.use_cases.comments.delete import DeleteCommentUseCase
from app.domain.use_cases.comments.list import ListCommentUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from app.infra.repositories.sqlalchemy.sqlalchemy_task_repository import SQLAlchemyTaskRepository


class CommentFactory:

    @staticmethod
    def repositories(session: AsyncSession):
        repository = SQLAlchemyCommentRepository(
            session
        )
        repository_task = SQLAlchemyTaskRepository(
            session
        )

        return repository, repository_task

    def create_comment_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> CreateCommentUseCase:
        return CreateCommentUseCase(
            *self.repositories(session)
        )

    def delete_comment_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> DeleteCommentUseCase:
        return DeleteCommentUseCase(
            *self.repositories(session)
        )

    def list_comments_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> ListCommentUseCase:
        return ListCommentUseCase(
            *self.repositories(session)
        )
