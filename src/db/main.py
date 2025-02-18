from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker


async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL
    )
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        from src.db.models import Book, User

        await conn.run_sync(
            SQLModel.metadata.create_all,
            tables=[Book.__tablename__, User.__tablename__]
        )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False)

    async with Session() as session:
        yield session
