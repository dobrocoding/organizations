from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import joinedload

from app.models.building import Building
from app.repos.base import SoftDeletableRepo

if TYPE_CHECKING:
    pass


class BuildingRepo(SoftDeletableRepo[UUID, Building]):
    load_options: ClassVar[list[Any]] = [
        joinedload(Building.organizations),
    ]

    def get_buildings_in_radius(
        self, latitude: Decimal, longitude: Decimal, radius_km: Decimal
    ) -> Select[tuple[Building]]:
        distance_formula = (
            func.acos(
                func.sin(func.radians(latitude)) * func.sin(func.radians(Building.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(Building.latitude))
                * func.cos(func.radians(longitude) - func.radians(Building.longitude))
            )
            * 6371
        )  # Earth's radius in kilometers

        return select(Building).where(distance_formula <= radius_km).options(*self.load_options)

    def get_buildings_in_bounds(
        self, min_lat: Decimal, max_lat: Decimal, min_lng: Decimal, max_lng: Decimal
    ) -> Select[tuple[Building]]:
        return (
            select(Building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lng, max_lng),
            )
            .options(*self.load_options)
        )
