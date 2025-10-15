from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

__all__ = (
    'AsyncSessionLocal',
    'DATABASE_URL',
    'get_engine',
)

load_dotenv()

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@'
    f'db:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}'
)


def get_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url, echo=True, future=True)


AsyncSessionLocal = async_sessionmaker(
    get_engine(DATABASE_URL),
    expire_on_commit=False,
    class_=AsyncSession,
)
