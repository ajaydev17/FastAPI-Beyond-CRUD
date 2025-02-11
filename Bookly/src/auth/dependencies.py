from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException
from fastapi import status, Request, Depends
from src.db.redis import check_jti_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService
from typing import List, Any
from src.auth.models import User

# create an instance of the user service
user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": 'Token is invalid or expired',
                    "resolution": "Please provide a new access token"
                }
            )

        if await check_jti_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": 'Token is invalid or has been revoked',
                    "resolution": "Please provide a new access token"
                }
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Please provide an access token!'
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Please provide a refresh token!'
            )


# create an instance of access token bearer class
access_token_bearer = AccessTokenBearer()


async def get_current_user(
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource."
        )
