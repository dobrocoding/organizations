from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import joinedload

from app.models import OrganizationActivity
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization
from app.repos.base import SoftDeletableRepo
from app.schemas.base import Filter, OrFilterGroup

if TYPE_CHECKING:
    pass


class OrganizationRepo(SoftDeletableRepo[UUID, Organization]):
    load_options: ClassVar[list[Any]] = [
        joinedload(Organization.building),
        joinedload(Organization.phones),
        joinedload(Organization.activities).joinedload(Activity.parent),
        joinedload(Organization.activities).joinedload(Activity.children),
    ]

    def get_by_name(self, name: str) -> Select[tuple[Organization]]:
        """Get organizations by name."""
        return self.retrieve_by(filters=[Filter(field='name', op='ilike', value=f'%{name}%')])

    def get_by_building_id(self, building_id: str) -> Select[tuple[Organization]]:
        """Get organizations by building ID."""
        return self.retrieve_by(filters=[Filter(field='building_id', op='=', value=building_id)])

    def get_by_activity_id(self, activity_id: UUID) -> Select[tuple[Organization]]:
        return (
            select(Organization)
            .join(OrganizationActivity, Organization.id == OrganizationActivity.organization_id)
            .where(OrganizationActivity.activity_id == activity_id)
            .options(*self.load_options)
        )

    def search_organizations(self, query: str) -> Select[tuple[Organization]]:
        return self.retrieve_by(
            filters=[
                OrFilterGroup(
                    filters=[
                        Filter(field='name', op='ilike', value=f'%{query}%'),
                        Filter(field='description', op='ilike', value=f'%{query}%'),
                    ]
                )
            ]
        )

    def get_organizations_in_radius(
        self, latitude: Decimal, longitude: Decimal, radius_km: Decimal
    ) -> Select[tuple[Organization]]:
        distance_formula = (
            func.acos(
                func.sin(func.radians(latitude)) * func.sin(func.radians(Building.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(Building.latitude))
                * func.cos(func.radians(longitude) - func.radians(Building.longitude))
            )
            * 6371
        )  # Earth's radius in kilometers

        return (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(distance_formula <= radius_km)
            .options(*self.load_options)
        )

    def get_organizations_in_bounds(
        self, min_lat: Decimal, max_lat: Decimal, min_lng: Decimal, max_lng: Decimal
    ) -> Select[tuple[Organization]]:
        return (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lng, max_lng),
            )
            .options(*self.load_options)
        )
