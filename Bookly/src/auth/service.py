from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreateSchema
from src.auth.utils import generate_password_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def check_user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user else False

    async def create_user(self,
                          user_data: UserCreateSchema,
                          session: AsyncSession):
        user_data_dict = user_data.model_dump()
        user = User(**user_data_dict)

        password = generate_password_hash(user_data_dict['password'])
        user.password_hash = password
        user.role = 'user'

        session.add(user)
        await session.commit()
        return user
