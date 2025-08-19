from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building
from app.repos.building import BuildingRepo
from app.schemas import BuildingResponseSchema
from app.services.base import SoftDeletableService


class BuildingService(SoftDeletableService[UUID, Building, BuildingResponseSchema]):
    response_schema = BuildingResponseSchema

    def __init__(self, repo: BuildingRepo) -> None:
        super().__init__(repo)
        self.repo: BuildingRepo = repo

    async def get_buildings_in_radius(
        self, session: AsyncSession, latitude: Decimal, longitude: Decimal, radius_km: Decimal
    ) -> list[BuildingResponseSchema]:
        """Get buildings within a given radius from a specified point."""
        query = self.repo.get_buildings_in_radius(latitude, longitude, radius_km)
        buildings = await session.scalars(query)
        return [self.response_schema.model_validate(building) for building in buildings]

    async def get_buildings_in_bounds(
        self,
        session: AsyncSession,
        min_lat: Decimal,
        max_lat: Decimal,
        min_lng: Decimal,
        max_lng: Decimal,
    ) -> list[BuildingResponseSchema]:
        """Get buildings within a rectangular area on the map."""
        query = self.repo.get_buildings_in_bounds(min_lat, max_lat, min_lng, max_lng)
        buildings = await session.scalars(query)
        return [self.response_schema.model_validate(building) for building in buildings]
