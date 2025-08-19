from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repos.organization import OrganizationRepo
from app.schemas import (
    Filter,
    OrganizationResponseSchema,
)
from app.schemas.organization import OrganizationDetailResponseSchema
from app.services.base import SoftDeletableService
from app.services.building import BuildingService
from app.services.phone import PhoneService


class OrganizationService(SoftDeletableService[UUID, Organization, OrganizationResponseSchema]):
    response_schema = OrganizationResponseSchema

    def __init__(
        self,
        repo: OrganizationRepo,
        phone_service: PhoneService,
        building_service: BuildingService,
    ) -> None:
        super().__init__(repo)
        self.repo: OrganizationRepo = repo
        self.phone_service: PhoneService = phone_service
        self.building_service: BuildingService = building_service

    async def get_organizations_by_name(
        self,
        session: AsyncSession,
        name: str,
    ) -> list[OrganizationResponseSchema]:
        query = self.repo.get_by_name(name)
        result = await session.execute(query)
        results = result.unique().scalars().all()
        return self.serialize_many(results)

    async def get_organizations_by_building(
        self,
        session: AsyncSession,
        building_id: UUID,
    ) -> list[OrganizationResponseSchema]:
        await self.building_service.retrieve(session, building_id)
        return await self.retrieve_all_by(
            db_session=session, filters=(Filter(field='building_id', value=building_id),)
        )

    async def get_organizations_by_activity(
        self,
        session: AsyncSession,
        activity_id: UUID,
    ) -> list[OrganizationResponseSchema]:
        query = self.repo.get_by_activity_id(activity_id)
        result = await session.execute(query)
        results = result.unique().scalars().all()
        return self.serialize_many(results)

    async def search_organizations(
        self,
        session: AsyncSession,
        query: str,
    ) -> list[OrganizationResponseSchema]:
        search_query = self.repo.search_organizations(query)
        result = await session.execute(search_query)
        results = result.unique().scalars().all()
        return self.serialize_many(results)

    async def get_organizations_in_radius(
        self,
        session: AsyncSession,
        latitude: Decimal,
        longitude: Decimal,
        radius_km: Decimal,
    ) -> list[OrganizationResponseSchema]:
        query = self.repo.get_organizations_in_radius(latitude, longitude, radius_km)
        result = await session.execute(query)
        results = result.unique().scalars().all()
        return self.serialize_many(results)

    async def get_organizations_in_bounds(
        self,
        session: AsyncSession,
        min_lat: Decimal,
        max_lat: Decimal,
        min_lng: Decimal,
        max_lng: Decimal,
    ) -> list[OrganizationResponseSchema]:
        query = self.repo.get_organizations_in_bounds(min_lat, max_lat, min_lng, max_lng)
        result = await session.execute(query)
        results = result.unique().scalars().all()
        return self.serialize_many(results)

    async def get_organization_detail(
        self,
        session: AsyncSession,
        organization_id: UUID,
    ) -> OrganizationDetailResponseSchema:
        organization = await self.retrieve_raw(session, organization_id)
        return OrganizationDetailResponseSchema.model_validate(organization)
