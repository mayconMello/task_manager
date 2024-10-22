from typing import Optional

from faker import Faker
from pydantic import BaseModel

from app.domain.entities.user import UserCreate

fake = Faker()


class OverrideUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


def make_user(override: OverrideUser = OverrideUser()) -> UserCreate:
    return UserCreate(
        name=override.name or fake.name(),
        email=override.email or fake.email(),
        password=override.password or fake.password(),
    )
