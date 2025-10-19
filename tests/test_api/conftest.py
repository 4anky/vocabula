from typing import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from vocabula.db import Base


@pytest.fixture(autouse=True)
async def _clear_database(db_engine: AsyncEngine) -> AsyncIterator[None]:
    """Creates the actual DB schema before each test and removes all after one."""
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield
