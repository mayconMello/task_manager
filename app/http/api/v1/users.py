from fastapi import APIRouter, Depends, status

from app.domain.entities.user import User, UserCreate
from app.domain.use_cases.users.create import CreateUserUseCase
from app.infra.factories.user_factory import UserFactory

router = APIRouter(tags=["Users"])

user_factory = UserFactory()


@router.post(
    '/',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create(
        body: UserCreate,
        use_case: CreateUserUseCase = Depends(user_factory.create_user_use_case)
):
    """
    Create a new user.
    """
    user = await use_case.execute(body)

    return user
