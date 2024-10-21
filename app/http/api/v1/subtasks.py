from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends

from app.core.auth import get_current_user
from app.domain.entities.subtask import Subtask, SubtaskUpdate
from app.domain.use_cases.subtasks.create import CreateSubtaskUseCase
from app.domain.use_cases.subtasks.delete import DeleteSubtaskUseCase
from app.domain.use_cases.subtasks.get import GetSubtaskUseCase
from app.domain.use_cases.subtasks.list import ListSubtaskUseCase
from app.domain.use_cases.subtasks.update import UpdateSubtaskUseCase
from app.infra.factories.subtask_factory import SubtaskFactory

router = APIRouter(tags=["Subtasks"])

subtask_factory = SubtaskFactory()


@router.post("/{task_id}/subtasks", response_model=Subtask, status_code=status.HTTP_201_CREATED)
async def create(
        task_id: str,
        body: Subtask,
        use_case: CreateSubtaskUseCase = Depends(subtask_factory.create_subtask_use_case),
        current_user: str = Depends(get_current_user)
):
    subtask = await use_case.execute(current_user, task_id, body)

    return subtask


@router.get("/{task_id}/subtasks/{subtask_id}", response_model=Subtask)
async def get(
        task_id: str,
        subtask_id: str,
        use_case: GetSubtaskUseCase = Depends(subtask_factory.get_subtask_use_case),
        current_user: str = Depends(get_current_user)
):
    subtask = await use_case.execute(current_user, task_id, subtask_id)

    return subtask


@router.get('/{task_id}/subtasks', response_model=List[Subtask])
async def list_subtasks(
        task_id: str,
        use_case: ListSubtaskUseCase = Depends(subtask_factory.list_subtasks_use_case),
        current_user: str = Depends(get_current_user)
):
    subtasks = await use_case.execute(current_user, task_id)
    return subtasks


@router.delete('/{task_id}/subtasks/{subtask_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        task_id: str,
        subtask_id: str,
        use_case: DeleteSubtaskUseCase = Depends(subtask_factory.delete_subtask_use_case),
        current_user: str = Depends(get_current_user)
):
    await use_case.execute(current_user, task_id, subtask_id)


@router.put('/{task_id}/subtasks/{subtask_id}', response_model=Subtask)
async def update(
        task_id: str,
        subtask_id: str,
        body: SubtaskUpdate,
        use_case: UpdateSubtaskUseCase = Depends(subtask_factory.update_subtask_use_case),
        current_user: str = Depends(get_current_user)
):
    subtask = await use_case.execute(
        current_user,
        task_id,
        subtask_id,
        body
    )

    return subtask
