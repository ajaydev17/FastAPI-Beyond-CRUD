from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.auth.schemas import UserCreateSchema, UserViewSchema
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

# define the router
auth_router = APIRouter()

# user service instance
user_service = UserService()


@auth_router.post('/signup',
                  response_model=UserViewSchema,
                  status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    is_user_exists = await user_service.check_user_exists(email, session)

    if is_user_exists:
        raise HTTPException(detail='User with email already exists.',
                            status_code=status.HTTP_403_FORBIDDEN)

    user = await user_service.create_user(user_data, session)
    return user
