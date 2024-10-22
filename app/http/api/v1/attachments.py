from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, Request

from app.core.auth import get_current_user
from app.domain.entities.attachment import Attachment
from app.domain.use_cases.attachments.create import CreateAttachmentUseCase
from app.domain.use_cases.attachments.delete import DeleteAttachmentUseCase
from app.domain.use_cases.attachments.list import ListAttachmentsUseCase
from app.infra.factories.attachment_factory import AttachmentFactory

router = APIRouter(tags=["Attachments"])

attachment_factory = AttachmentFactory()


def serializer_attachment(attachment: Attachment, request: Request) -> Attachment:
    attachment.set_request_context(request)

    return attachment


@router.post(
    "/{task_id}/attachments",
    response_model=Attachment,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    task_id: str,
    file: UploadFile,
    request: Request,
    use_case: CreateAttachmentUseCase = Depends(attachment_factory.create_attachment_use_case),
    current_user: str = Depends(get_current_user),
):
    attachment = await use_case.execute(current_user, task_id, file)

    return serializer_attachment(attachment, request)


@router.get("/{task_id}/attachments", response_model=List[Attachment])
async def list_attachments(
    task_id: str,
    request: Request,
    use_case: ListAttachmentsUseCase = Depends(attachment_factory.list_attachments_use_case),
    current_user: str = Depends(get_current_user),
):
    attachments = await use_case.execute(
        current_user,
        task_id,
    )

    attachments = [serializer_attachment(attachment, request) for attachment in attachments]

    return attachments


@router.delete("/{task_id}/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: str,
    attachment_id: str,
    use_case: DeleteAttachmentUseCase = Depends(attachment_factory.delete_attachment_use_case),
    current_user: str = Depends(get_current_user),
):
    await use_case.execute(
        current_user,
        task_id,
        attachment_id,
    )
