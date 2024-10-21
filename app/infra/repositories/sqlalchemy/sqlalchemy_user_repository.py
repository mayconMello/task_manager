from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.user import User, UserCreate
from app.infra.db.models import UserModel
from app.infra.repositories.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return User.model_validate(db_user)

    async def get_by_id(self, user_id: UUID4) -> User | None:
        user = await self.session.get(UserModel, user_id)

        return User.model_validate(user)

    async def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)

        user = result.scalar_one_or_none()

        if user:
            return User.model_validate(user)

        return user
