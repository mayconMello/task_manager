from fastapi import APIRouter, Depends, Response, Cookie
from pydantic import BaseModel

from app.core.auth import create_jwt_token, decode_token, create_jwt_refresh_token
from app.domain.entities.authenticate import Authenticate
from app.domain.use_cases.session.authenticate import AuthenticateUseCase
from app.domain.use_cases.users.get_by_id import GetUserByIdUseCase
from app.infra.factories.session_factory import SessionFactory
from app.infra.factories.user_factory import UserFactory

router = APIRouter(tags=["Session"])

session_factory = SessionFactory()
user_factory = UserFactory()


class Token(BaseModel):
    access_token: str


@router.post("/", response_model=Token)
async def create_session(
    response: Response,
    body: Authenticate,
    use_case: AuthenticateUseCase = Depends(session_factory.authenticate_use_case),
):
    user = await use_case.execute(body)

    access_token = create_jwt_token(user.id)
    refresh_token = create_jwt_refresh_token(user.id)

    token = Token(access_token=access_token)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return token


@router.post(
    "/refresh",
)
async def refresh_session(
    response: Response,
    refresh_token: str = Cookie(None),
    use_case: GetUserByIdUseCase = Depends(user_factory.get_user_by_id_use_case),
):
    sub = decode_token(refresh_token)

    user = await use_case.execute(sub)

    access_token = create_jwt_token(user.id)
    refresh_token = create_jwt_refresh_token(user.id)

    token = Token(
        access_token=access_token,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return token
