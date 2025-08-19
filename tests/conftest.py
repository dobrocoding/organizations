from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.asgi import app as asgi_app
from app.core.containers import AppContainer
from app.dependencies.db_session import get_db_session


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return asgi_app


@pytest.fixture(scope='session')
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
def api_token() -> str:
    """Return the API token for testing."""
    return 'Secunda_demo_token'


@pytest.fixture(scope='session')
def api_headers(api_token: str) -> dict[str, str]:
    """Return headers with API token for testing."""
    return {'Authorization': f'Bearer {api_token}'}


@pytest.fixture(scope='session')
async def db_engine() -> AsyncIterator[AsyncEngine]:
    yield await AppContainer.db_engine()


@pytest.fixture(scope='session')
async def session_factory() -> AsyncIterator[async_sessionmaker]:
    yield await AppContainer.session_factory()


@pytest.fixture(scope='session')
async def redis() -> Redis:
    return await AppContainer.global_redis()


@pytest.fixture(autouse=True)
async def db_session(
    app: FastAPI,
    session_factory: async_sessionmaker,
) -> AsyncIterator[AsyncSession]:
    async_session = session_factory()
    app.dependency_overrides[get_db_session] = lambda: async_session
    yield async_session
    await async_session.rollback()
    await async_session.close()


@pytest.fixture(scope='session', autouse=True)
async def init_db(db_engine: AsyncEngine) -> None:
    """Restart all sequences from database.

    Called one time for all tests.
    Cleans up "global_id_sequence" in addition to table sequences,
    so just TRUNCATE TABLE ... RESTART IDENTITY CASCADE wouldn't be enough.
    """
    async with db_engine.begin() as conn:
        stmt = text("SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';")
        sequences = (await conn.execute(stmt)).scalars().all()
        for sequence in sequences:
            await conn.execute(text(f'ALTER SEQUENCE {sequence} RESTART;'))


@pytest.fixture(autouse=True)
async def clean_all_tables(db_engine: AsyncEngine) -> None:
    """Clean all tables before tests and after every test."""
    stmt = text("SELECT t.table_name FROM information_schema.tables t WHERE table_schema='public'")
    async with db_engine.begin() as conn:
        tables = (await conn.execute(stmt)).scalars().all()
        tables = [
            t_name
            for t_name in tables
            if not t_name.startswith('pg_')
            and not t_name.startswith('v_')
            and not t_name.startswith('alembic')
        ]
        for table_name in tables:
            await conn.execute(text(f'TRUNCATE TABLE "{table_name}" CASCADE;'))


@pytest.fixture(autouse=True)
async def clean_redis(redis: Redis) -> None:
    """Clean all redis before tests and after every test."""
    await redis.flushall()
