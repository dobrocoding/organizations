from collections.abc import AsyncIterator
from typing import cast

import pytest
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.containers import AppContainer
from tests.test_integration.mocks.model import MockModel
from tests.test_integration.mocks.repo import MockRepo
from tests.test_integration.mocks.schema import MockModelResponseSchema
from tests.test_integration.mocks.service import MockService


@pytest.fixture(scope='session')
async def db_engine() -> AsyncIterator[AsyncEngine]:
    yield await AppContainer.db_engine()


@pytest.fixture(scope='session', autouse=True)
async def setup_db(db_engine: AsyncEngine) -> None:
    async with db_engine.begin() as conn:
        await conn.run_sync(cast(Table, MockModel.__table__).create, checkfirst=True)


@pytest.fixture(scope='function')
def mock_repo() -> MockRepo:
    return MockRepo(MockModel)


@pytest.fixture(scope='function')
def mock_service(mock_repo: MockRepo) -> MockService:
    service = MockService(mock_repo)
    service.response_schema = MockModelResponseSchema
    return service
