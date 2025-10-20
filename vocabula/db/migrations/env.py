import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from vocabula.db import DATABASE_URL

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# We receive DATABASE_URL from tests
if os.environ.get('DATABASE_URL') is not None:
    DATABASE_URL = os.environ.get('DATABASE_URL')

config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
else:
    raise ValueError('No configuration file specified')


# ensure project root is on path (so imports like "app.*" работают)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import vocabula.models.users  # noqa: F401 (импортирует модель и регистрирует её в Base.metadata)

# Импортируем metadata от Base и модели — важно,
# чтобы автоматическая генерация видела таблицы
from vocabula.db.base import Base  # noqa: E402,F401

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # полезно для обнаружения изменения типов колонок
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Run sync migration functions in a connection via run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
