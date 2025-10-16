from os import environ
from pathlib import Path
from typing import AsyncIterator, Iterator

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from vocabula.db import Base, get_db, get_engine
from vocabula.main import app

load_dotenv(Path(__file__).parent.parent / '.env')


@pytest.fixture(scope='session')
def _db_container() -> Iterator[PostgresContainer]:
    """Returns the object of the Postgres database container."""
    with PostgresContainer(
        'postgres:16',
        username=environ['POSTGRES_USER'],
        password=environ['POSTGRES_PASSWORD'],
        dbname=environ['POSTGRES_DB'],
        driver='asyncpg',
    ) as postgres:
        yield postgres


@pytest.fixture
def db_engine(_db_container: PostgresContainer) -> AsyncEngine:
    return get_engine(_db_container.get_connection_url())


@pytest.fixture(autouse=True)
async def _clear_database(db_engine: AsyncEngine) -> AsyncIterator[None]:
    """Creates the actual DB schema before each test and removes all after one."""
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
def _session_factory(db_engine) -> async_sessionmaker:
    return async_sessionmaker(
        db_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
async def db_session(_session_factory) -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        yield session


@pytest.fixture
async def client(db_session) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_db] = lambda: db_session  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as client:
        yield client
    app.dependency_overrides.clear()  # type: ignore[attr-defined]
