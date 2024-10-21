from pydantic import BaseModel, Field


class Authenticate(BaseModel):
    email: str
    password: str = Field(min_length=8, exclude=True)
