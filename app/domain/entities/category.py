from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4


class Category(BaseModel):
    id: Optional[UUID4] = None
    name: str

    model_config = ConfigDict(from_attributes=True)
