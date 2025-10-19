from os import environ
from pathlib import Path
from typing import AsyncIterator, Iterator

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from vocabula.db import get_db, get_engine
from vocabula.main import app

load_dotenv(Path(__file__).parent.parent / '.env')


@pytest.fixture(scope='session')
def project_root_path() -> Path:
    project_root = Path(__file__).parent.parent
    assert project_root.exists() and project_root.name == 'vocabula'
    return project_root


@pytest.fixture(scope='session')
def _db_container() -> Iterator[PostgresContainer]:
    """Returns the object of the Postgres database container."""
    with PostgresContainer(
        'postgres:16',
        username=environ['POSTGRES_USER'],
        dbname=environ['POSTGRES_DB'],
        driver='asyncpg',
    ) as postgres:
        yield postgres


@pytest.fixture
def db_engine(_db_container: PostgresContainer) -> AsyncEngine:
    return get_engine(_db_container.get_connection_url())


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
