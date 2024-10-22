from typing import List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.comment import Comment
from app.infra.db.models import CommentModel
from app.infra.repositories.comment_repository import CommentRepository


class SQLAlchemyCommentRepository(CommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        comment_db = CommentModel(
            content=comment.content,
            task_id=comment.task_id,
            user_id=comment.user_id,
        )

        self.session.add(comment_db)
        await self.session.commit()
        await self.session.refresh(comment_db)

        return Comment.model_validate(comment_db)

    async def delete(self, task_id: UUID4, comment_id: UUID4):
        query = (
            select(CommentModel)
            .where(
                CommentModel.task_id == task_id,
            )
            .where(CommentModel.id == comment_id)
        )
        result = await self.session.execute(query)

        comment = result.scalar()

        await self.session.delete(comment)
        await self.session.commit()

    async def get(self, task_id: UUID4, comment_id: UUID4) -> Comment | None:
        query = (
            select(CommentModel)
            .where(
                CommentModel.task_id == task_id,
            )
            .where(CommentModel.id == comment_id)
        )
        result = await self.session.execute(query)

        comment = result.scalar_one_or_none()

        if comment:
            return Comment.model_validate(comment)

        return comment

    async def list(self, task_id: UUID4) -> List[Comment]:
        query = select(CommentModel).where(
            CommentModel.task_id == task_id,
        )
        result = await self.session.execute(query)

        comments = result.scalars().all()

        return list(map(Comment.model_validate, comments))
