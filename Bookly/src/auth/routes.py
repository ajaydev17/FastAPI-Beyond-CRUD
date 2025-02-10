from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.auth.schemas import UserCreateSchema, UserViewSchema, UserLoginSchema
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import (
    create_access_token,
    verify_password_hash
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer

# define the router
auth_router = APIRouter()

# user service instance
user_service = UserService()

# create the instance of refresh token class
refresh_token_bearer = RefreshTokenBearer()

REFRESH_TOKEN_EXPIRY = 2


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


@auth_router.post('/login')
async def login(
    user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        valid_password = verify_password_hash(
            password,
            user.password_hash
        )

        if valid_password:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    'message': 'Login Successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'user_id': str(user.uid)
                    }
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid email or password'
    )


@auth_router.get('/refresh_token')
async def get_new_access_token(
    token_details: dict = Depends(refresh_token_bearer)
):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(
            content={
                "access_token": access_token
            }
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Invalid or expired token!'
    )
