from typing import Optional, Literal

from faker import Faker
from pydantic import BaseModel

from app.domain.entities.user import User, UserCreate

fake = Faker()


class OverrideUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal['ADMIN', 'MEMBER']] = 'MEMBER'


def make_user(override: OverrideUser = OverrideUser()) -> UserCreate:
    return UserCreate(
        name=override.name or fake.name(),
        email=override.email or fake.email(),
        password=override.password or fake.password(),
        role=override.role or 'MEMBER'
    )
