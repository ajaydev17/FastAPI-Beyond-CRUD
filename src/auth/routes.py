from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.auth.schemas import (
    UserCreateSchema, 
    UserViewSchema, 
    UserLoginSchema,
    UserBookViewSchema
)
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import (
    create_access_token,
    verify_password_hash
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker
)
from src.db.redis import add_jti_to_blocklist
from src.errors import (
    InvalidToken,
    InvalidCredentials,
    UserAlreadyExists
)

# define the router
auth_router = APIRouter()

# user service instance
user_service = UserService()

# role checker
role_checker = RoleChecker(['admin', 'user'])

# create the instance of refresh token class, access token class
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post('/signup',
                  response_model=UserViewSchema,
                  status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateSchema,
    session: AsyncSession = Depends(get_session)
) -> UserViewSchema:
    email = user_data.email

    is_user_exists = await user_service.check_user_exists(email, session)

    if is_user_exists:
        raise UserAlreadyExists()

    user = await user_service.create_user(user_data, session)
    return user


@auth_router.post('/login')
async def login(
    user_data: UserLoginSchema,
    session: AsyncSession = Depends(get_session)
) -> dict:
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
                    'user_uid': str(user.uid),
                    'role': user.role
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
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
                        'user_uid': str(user.uid)
                    }
                }
            )

    raise InvalidCredentials()


@auth_router.get('/refresh_token')
async def get_new_access_token(
    token_details: dict = Depends(refresh_token_bearer)
) -> dict:
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

    raise InvalidToken()


@auth_router.post('/logout')
async def logout(
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logout successful"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.get('/me', response_model=UserBookViewSchema)
async def get_current_user_details(
    current_user: UserViewSchema = Depends(get_current_user),
    _: bool = Depends(role_checker)
) -> UserBookViewSchema:
    return current_user
