from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker


async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(Book.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False)

    async with Session() as session:
        yield session
