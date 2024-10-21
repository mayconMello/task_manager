from abc import ABC, abstractmethod
from typing import List

from pydantic import UUID4

from app.domain.entities.comment import Comment


class CommentRepository(ABC):

    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def list(self, task_id: UUID4) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: UUID4, comment_id: UUID4) -> Comment | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: UUID4, comment_id: UUID4):
        raise NotImplementedError
