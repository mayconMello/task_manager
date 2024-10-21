from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.session.authenticate import AuthenticateUseCase
from app.domain.use_cases.users.create import CreateUserUseCase
from app.domain.use_cases.users.get_by_id import GetUserByIdUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository


class UserFactory:

    @staticmethod
    def repository(session: AsyncSession) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(session)

    def create_user_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> CreateUserUseCase:
        return CreateUserUseCase(self.repository(session))

    def get_user_by_id_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> GetUserByIdUseCase:
        return GetUserByIdUseCase(self.repository(session))

    def authenticate_user_use_case(
            self,
            session: AsyncSession = Depends(get_session)
    ) -> AuthenticateUseCase:
        return AuthenticateUseCase(self.repository(session))
