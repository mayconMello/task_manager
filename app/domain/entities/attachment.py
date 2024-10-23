from typing import Optional

from fastapi import Request
from pydantic import BaseModel, UUID4, ConfigDict, computed_field, Field

from app.core.configs import settings


class Attachment(BaseModel):
    request: Request = Field(
        default=None,
        exclude=True,
    )

    id: Optional[UUID4] = None
    original_name: str
    filename: str
    file_path: str
    task_id: Optional[UUID4] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def set_request_context(self, request: Request):
        self.request = request

    @computed_field
    @property
    def url(self) -> str:
        if self.request is None:
            return f"/{settings.MEDIA_URL}/{self.filename}"

        url = self.request.url_for(settings.MEDIA_URL, path=self.filename)
        return str(url)
