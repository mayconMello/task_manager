from app.domain.entities.task import Task, TaskCreate
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository


class CreateTaskUseCase:
    def __init__(
        self,
        repository: TaskRepository,
        repository_user: UserRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user

    async def execute(self, user_id: str, body: TaskCreate) -> Task:
        user = await self.repository_user.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError()

        body.user_id = user.id
        task = await self.repository.create(body)

        return task
