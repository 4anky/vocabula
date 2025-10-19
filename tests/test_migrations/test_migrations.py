import asyncio
from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine
from testcontainers.postgres import PostgresContainer

from vocabula.db import Base
from vocabula.models import User


@pytest.mark.asyncio
async def test_models_match_migrations(
    _db_container: PostgresContainer,
    db_engine: AsyncEngine,
    db_session,
    project_root_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Ensures that SQLAlchemy Metadata matches the DB state after Alembic migrations."""
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    async with db_engine.begin() as connection:
        with pytest.raises(ProgrammingError):
            _ = await connection.execute(select(User))

    async_url = str(_db_container.get_connection_url())
    sync_url = async_url.replace('+asyncpg', '')

    monkeypatch.setenv('DATABASE_URL', async_url)
    alembic_config = Config(project_root_path / 'alembic.ini')
    await asyncio.to_thread(command.upgrade, alembic_config, 'head')

    sync_engine: Engine = create_engine(sync_url)
    with sync_engine.connect() as conn:
        context = MigrationContext.configure(connection=conn)
        diff = compare_metadata(context, Base.metadata)

    assert diff == [], f'Database schema differs from models: {diff}'
