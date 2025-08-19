from typing import Any
from uuid import UUID

from app.models.organization_activity import OrganizationActivity
from tests.factories.base import SQLAlchemyBaseModelFactory


class OrganizationActivityFactory(SQLAlchemyBaseModelFactory[OrganizationActivity]):
    __model__ = OrganizationActivity

    @classmethod
    def build_with_ids(
        cls, organization_id: UUID, activity_id: UUID, **kwargs: Any
    ) -> OrganizationActivity:
        return cls.build(organization_id=organization_id, activity_id=activity_id, **kwargs)
