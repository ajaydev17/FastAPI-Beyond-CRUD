from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config


engine = AsyncEngine(
    create_engine(
        url=config.DATABASE_URL,
        echo=True
    )
)
