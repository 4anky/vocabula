from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

__all__ = (
    'engine',
    'AsyncSessionLocal',
    'DATABASE_URL',
)

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@'
    f'db:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}'
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
