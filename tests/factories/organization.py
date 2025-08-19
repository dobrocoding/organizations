from typing import Any
from uuid import UUID

from polyfactory import Use

from app.models.organization import Organization
from tests.factories.base import SQLAlchemyBaseModelFactory


class OrganizationFactory(SQLAlchemyBaseModelFactory[Organization]):
    __model__ = Organization

    name = Use(lambda: f'Organization {OrganizationFactory.__faker__.company()}')
    description = Use(lambda: OrganizationFactory.__faker__.sentence())  # noqa: PLW0108
    website = Use(lambda: OrganizationFactory.__faker__.url())  # noqa: PLW0108
    email = Use(lambda: OrganizationFactory.__faker__.email())  # noqa: PLW0108

    @classmethod
    def build_with_building(cls, building_id: UUID, **kwargs: Any) -> Organization:
        return cls.build(building_id=building_id, **kwargs)
