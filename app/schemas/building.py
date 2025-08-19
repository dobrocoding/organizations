from decimal import Decimal
from uuid import UUID

from app.schemas import AdminMeta, BaseResponseSchema


class BaseBuildingResponseSchema(BaseResponseSchema):
    id: UUID
    address: str
    latitude: Decimal
    longitude: Decimal
    name: str | None
    description: str | None


class BuildingResponseSchema(BaseBuildingResponseSchema, AdminMeta): ...
