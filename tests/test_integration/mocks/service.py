from uuid import UUID

from app.services.base import SoftDeletableService
from tests.test_integration.mocks.model import MockModel
from tests.test_integration.mocks.schema import MockModelResponseSchema


class MockService(SoftDeletableService[UUID, MockModel, MockModelResponseSchema]): ...
