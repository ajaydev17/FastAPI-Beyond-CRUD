from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging

passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    passwd_hash = passwd_context.hash(password)
    return passwd_hash


def verify_password_hash(password: str, passwd_hash: str) -> bool:
    return passwd_context.verify(password, passwd_hash)


def create_access_token(
        user_data: dict,
        expiry: timedelta = None,
        refresh: bool = False
):
    payload = {'user': user_data, 'exp': datetime.now() + (
        expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    ), 'jti': str(uuid.uuid4()), 'refresh': refresh}

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

