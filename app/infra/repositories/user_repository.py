from abc import ABC, abstractmethod

from pydantic import UUID4

from app.domain.entities.user import User, UserCreate


class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID4) -> User | None:
        raise NotImplementedError
