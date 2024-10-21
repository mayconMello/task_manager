from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, ConfigDict, UUID4


class User(BaseModel):
    id: Optional[UUID4] = None
    name: str
    email: str
    password: str = Field(exclude=True)
    role: Literal["ADMIN", "MEMBER"] = "MEMBER"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreate(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=6)

    model_config = ConfigDict(
        from_attributes=True
    )
