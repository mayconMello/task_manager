from typing import List

from fastapi import APIRouter, status, Depends

from app.core.auth import get_current_user
from app.domain.entities.comment import Comment
from app.domain.use_cases.comments.create import CreateCommentUseCase
from app.domain.use_cases.comments.delete import DeleteCommentUseCase
from app.domain.use_cases.comments.list import ListCommentUseCase
from app.infra.factories.comment_factory import CommentFactory

router = APIRouter(tags=["Comments"])

comment_factory = CommentFactory()


@router.post("/{task_id}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create(
    task_id: str,
    body: Comment,
    use_case: CreateCommentUseCase = Depends(comment_factory.create_comment_use_case),
    current_user: str = Depends(get_current_user),
):
    comment = await use_case.execute(current_user, task_id, body)

    return comment


@router.get("/{task_id}/comments", response_model=List[Comment])
async def list_comments(
    task_id: str,
    use_case: ListCommentUseCase = Depends(comment_factory.list_comments_use_case),
    current_user: str = Depends(get_current_user),
):
    comments = await use_case.execute(
        current_user,
        task_id,
    )

    return comments


@router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: str,
    comment_id: str,
    use_case: DeleteCommentUseCase = Depends(comment_factory.delete_comment_use_case),
    current_user: str = Depends(get_current_user),
):
    await use_case.execute(current_user, task_id, comment_id)
