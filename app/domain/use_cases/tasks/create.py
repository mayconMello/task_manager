from app.domain.entities.task import Task, TaskCreate
from app.domain.errors import ResourceNotFoundError
from app.infra.repositories.task_repository import TaskRepository
from app.infra.repositories.user_repository import UserRepository
from app.infra.repositories.category_repository import CategoryRepository


class CreateTaskUseCase:
    def __init__(
        self,
        repository: TaskRepository,
        repository_user: UserRepository,
        repository_category: CategoryRepository,
    ):
        self.repository = repository
        self.repository_user = repository_user
        self.repository_category = repository_category

    async def execute(self, user_id: str, body: TaskCreate) -> Task:
        user = await self.repository_user.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError('User does not exist')

        category = await self.repository_category.get(body.category_id)
        if not category:
            raise ResourceNotFoundError('Category not found')

        body.user_id = user.id
        task = await self.repository.create(body)

        return task
