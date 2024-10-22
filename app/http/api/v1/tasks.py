from typing import List

from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.domain.entities.task import Task, TaskUpdateStatus, TaskUpdate, TaskCreate
from app.domain.use_cases.tasks.create import CreateTaskUseCase
from app.domain.use_cases.tasks.delete import DeleteTaskUseCase
from app.domain.use_cases.tasks.get import GetTaskUseCase
from app.domain.use_cases.tasks.list import ListTasksUseCase, TaskListFilter
from app.domain.use_cases.tasks.list_due_soon import ListTasksDueSoonUseCase
from app.domain.use_cases.tasks.update import UpdateTaskUseCase
from app.domain.use_cases.tasks.update_status import UpdateStatusTaskUseCase
from app.infra.factories.task_factory import TaskUseCaseFactory

router = APIRouter(tags=["Tasks"])

task_factory = TaskUseCaseFactory()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create(
    body: TaskCreate,
    use_case: CreateTaskUseCase = Depends(task_factory.create_task_use_case),
    current_user_id: str = Depends(get_current_user),
):
    task = await use_case.execute(current_user_id, body)

    return task


@router.get("/", response_model=List[Task])
async def list_tasks(
    params: TaskListFilter = Depends(),
    use_case: ListTasksUseCase = Depends(task_factory.list_tasks_use_case),
    current_user_id: str = Depends(get_current_user),
):
    tasks = await use_case.execute(current_user_id, params)
    return tasks


@router.get("/due-soon", response_model=List[Task])
async def list_due_soon(
    use_case: ListTasksDueSoonUseCase = Depends(task_factory.list_tasks_due_soon_use_case),
    current_user_id: str = Depends(get_current_user),
):
    tasks = await use_case.execute(current_user_id)
    return tasks


@router.get("/{task_id}", response_model=Task)
async def get(
    task_id: str,
    use_case: GetTaskUseCase = Depends(task_factory.get_task_use_case),
    current_user_id: str = Depends(get_current_user),
):
    task = await use_case.execute(task_id, current_user_id)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    task_id: str,
    use_case: DeleteTaskUseCase = Depends(task_factory.delete_task_use_case),
    current_user_id: str = Depends(get_current_user),
):
    await use_case.execute(task_id, current_user_id)


@router.put("/{task_id}", response_model=Task)
async def update(
    task_id: str,
    body: TaskUpdate,
    use_case: UpdateTaskUseCase = Depends(task_factory.update_task_use_case),
    current_user_id: str = Depends(get_current_user),
):
    task = await use_case.execute(task_id, current_user_id, body)
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_status(
    task_id: str,
    body: TaskUpdateStatus,
    use_case: UpdateStatusTaskUseCase = Depends(task_factory.update_status_task_use_case),
    current_user_id: str = Depends(get_current_user),
):
    task = await use_case.execute(task_id, current_user_id, is_completed=body.is_completed)
    return task
