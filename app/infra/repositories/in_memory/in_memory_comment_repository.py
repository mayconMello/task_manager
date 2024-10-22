import uuid
from datetime import datetime
from typing import List

from pydantic import UUID4

from app.domain.entities.comment import Comment
from app.infra.repositories.comment_repository import CommentRepository


class InMemoryCommentRepository(CommentRepository):
    def __init__(self):
        self.items: List[Comment] = []

    async def create(self, comment: Comment) -> Comment:
        comment.id = comment.id or uuid.uuid4()
        comment.created_at = datetime.now()
        self.items.append(comment)
        return comment

    async def list(self, task_id: UUID4) -> List[Comment]:
        comments = [comment for comment in self.items if comment.task_id == task_id]

        return comments

    async def get(self, task_id: UUID4, comment_id: UUID4) -> Comment | None:
        for item in self.items:
            if item.task_id == task_id and item.id == comment_id:
                return item

        return None

    async def delete(self, task_id: UUID4, comment_id: UUID4):
        for item in self.items:
            if item.task_id == task_id and item.id == comment_id:
                self.items.remove(item)
                return
