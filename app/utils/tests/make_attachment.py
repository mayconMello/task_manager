from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, UUID4

from app.domain.entities.attachment import Attachment

fake = Faker()


class OverrideAttachment(BaseModel):
    id: Optional[UUID4] = None
    original_name: Optional[str] = None
    filename: Optional[str] = None
    file_path: Optional[str] = None
    task_id: Optional[UUID4] = None


def make_attachment(override: OverrideAttachment = OverrideAttachment()) -> Attachment:
    return Attachment(
        id=override.id or uuid4(),
        original_name=override.original_name or fake.file_name(),
        filename=override.filename or fake.file_name(),
        file_path=override.file_path or fake.file_name(),
        task_id=override.task_id or uuid4(),
    )
