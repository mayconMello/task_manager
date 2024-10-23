from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from pwdlib import PasswordHash
from pydantic import UUID4

from app.core.configs import settings
from app.utils.datetime import get_utc_now

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt_token(sub: UUID4):
    expire = get_utc_now() + timedelta(minutes=settings.JWT_EXPIRES_TOKEN_IN_MINUTES)
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_jwt_refresh_token(sub: UUID4):
    expire = get_utc_now() + timedelta(
        minutes=settings.JWT_EXPIRES_REFRESH_TOKEN_IN_DAYS
    )
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> str:
    payload = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    sub = payload["sub"]

    return sub


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> str | HTTPException:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    sub = decode_token(token)
    if not sub:
        raise credentials_exception

    return sub
