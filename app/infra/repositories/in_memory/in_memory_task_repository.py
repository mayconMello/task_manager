import uuid
from datetime import datetime
from typing import List

from pydantic import UUID4

from app.domain.entities.task import Task, TaskUpdate, TaskCreate
from app.infra.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.items: List[Task] = []

    async def create(self, task: TaskCreate) -> Task:
        task_db = Task(
            **task.model_dump(),
            id=uuid.uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.items.append(task_db)

        return task_db

    async def list(self, user_id: str, params: dict) -> List[Task]:
        tasks = [
            item
            for item in self.items
            if item.user_id == user_id
        ]

        if not params:
            return tasks

        filtered_tasks = []
        for item in tasks:
            match = True
            for key, value in params.items():
                item_value = getattr(item, key, None)

                if isinstance(value, str) and isinstance(item_value, str):
                    if value.lower() not in item_value.lower():
                        match = False
                        break
                else:
                    if item_value != value:
                        match = False
                        break

            if match:
                filtered_tasks.append(item)

        return filtered_tasks

    async def list_due_soon(self, user_id: UUID4, due_time_limit: datetime) -> List[Task]:
        tasks = [
            item
            for item in self.items
            if item.user_id == user_id
        ]

        tasks_due_soon = [
            task
            for task in tasks
            if task.due_date and task.due_date <= due_time_limit
        ]

        return tasks_due_soon

    async def get(self, user_id: str, task_id: str) -> Task | None:
        for item in self.items:
            if item.user_id == user_id and item.id == task_id:
                return item

        return None

    async def delete(self, task_id: str) -> None:
        for item in self.items:
            if item.id == task_id:
                self.items.remove(item)

    async def update(self, task_id: str, task: TaskUpdate) -> Task:
        for index, item in enumerate(self.items):
            if item.id == task_id:
                item.title = task.title
                item.description = task.description
                item.due_date = task.due_date
                item.category_id = task.category_id
                item.updated_at = datetime.now()
                self.items[index] = item

                return item

    async def update_status(self, task_id: str, is_completed: bool) -> Task:
        for index, item in enumerate(self.items):
            if item.id == task_id:
                item.is_completed = is_completed
                item.updated_at = datetime.now()
                self.items[index] = item
                return item
