from typing import List
from uuid import uuid4

from app.domain.entities.user import User, UserCreate
from app.infra.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.items: List[User] = []

    async def create(self, user: UserCreate) -> User:
        db_user = User(id=uuid4(), **user.model_dump())
        self.items.append(db_user)

        return db_user

    async def get_by_email(self, email: str) -> User | None:
        for item in self.items:
            if item.email == email:
                return item

        return None

    async def get_by_id(self, user_id: str) -> User | None:
        for item in self.items:
            if item.id == user_id:
                return item

        return None
