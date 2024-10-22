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
    expire = get_utc_now() + timedelta(minutes=settings.jwt_expires_token_in_minutes)
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_jwt_refresh_token(sub: UUID4):
    expire = get_utc_now() + timedelta(minutes=settings.jwt_expires_refresh_token_in_days)
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_token(token: str) -> str:
    payload = decode(
        token,
        settings.secret_key,
        algorithms=[settings.jwt_algorithm],
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
