from .session import AsyncSessionLocal

__all__ = (
    'get_db',
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
