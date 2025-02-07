from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config


engine = AsyncEngine(
    create_engine(
        url=config.DATABASE_URL,
        echo=True
    )
)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(Book.metadata.create_all)
