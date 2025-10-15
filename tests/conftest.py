from os import environ
from pathlib import Path
from typing import AsyncIterator, Iterator

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from vocabula.db.session import get_engine
from vocabula.main import app

load_dotenv(Path(__file__).parent.parent / '.env')


@pytest.fixture(scope='session')
def _db_container() -> Iterator[PostgresContainer]:
    with PostgresContainer(
        'postgres:16',
        username=environ['POSTGRES_USER'],
        password=environ['POSTGRES_PASSWORD'],
        dbname=environ['POSTGRES_DB'],
        driver='asyncpg',
    ) as postgres:
        yield postgres


@pytest.fixture(scope='session')
def _session_factory(_db_container) -> async_sessionmaker:
    return async_sessionmaker(
        get_engine(_db_container.get_connection_url()),
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
async def db_session(_session_factory) -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        yield session


@pytest.fixture
async def client(db_session) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_engine] = lambda: db_session  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as client:
        yield client
    app.dependency_overrides.clear()  # type: ignore[attr-defined]
