from decimal import Decimal
from uuid import UUID

from app.schemas import AdminMeta, BaseRequestSchema, BaseResponseSchema
from app.schemas.activity import ActivityResponseSchema
from app.schemas.building import BuildingResponseSchema
from app.schemas.phone import PhoneResponseSchema


class BaseOrganizationResponseSchema(BaseResponseSchema):
    id: UUID
    name: str
    description: str | None
    website: str | None
    email: str | None


class OrganizationResponseSchema(BaseOrganizationResponseSchema, AdminMeta): ...


class OrganizationDetailResponseSchema(BaseOrganizationResponseSchema, AdminMeta):
    building: BuildingResponseSchema
    phones: list[PhoneResponseSchema]
    activities: list[ActivityResponseSchema]


class RadiusSearchRequestSchema(BaseRequestSchema):
    latitude: Decimal
    longitude: Decimal
    radius_km: Decimal


class BoundsSearchRequestSchema(BaseRequestSchema):
    min_lat: Decimal
    max_lat: Decimal
    min_lng: Decimal
    max_lng: Decimal
