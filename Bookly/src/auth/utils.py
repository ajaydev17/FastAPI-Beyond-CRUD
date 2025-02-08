from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=['bcrypt']
)


def generate_password_hash(password: str) -> str:
    passwd_hash = passwd_context.hash(password)
    return passwd_hash


def verify_password_hash(password: str, passwd_hash: str) -> bool:
    return passwd_context.verify(password, passwd_hash)
