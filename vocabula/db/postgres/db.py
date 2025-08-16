from asyncpg import Pool, create_pool

__all__ = (
    'connect_db',
    'disconnect_db',
)

_DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/yourdb"

db_pool: Pool | None = None


async def connect_db():
    global db_pool
    db_pool = await create_pool(_DATABASE_URL)


async def disconnect_db():
    await db_pool.close()
