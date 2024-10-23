from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.use_cases.session.authenticate import AuthenticateUseCase
from app.infra.db.session import get_session
from app.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


class SessionFactory:
    @staticmethod
    def repository(
        session: AsyncSession,
    ) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(session)

    def authenticate_use_case(
        self, session: AsyncSession = Depends(get_session)
    ) -> AuthenticateUseCase:
        return AuthenticateUseCase(self.repository(session))
