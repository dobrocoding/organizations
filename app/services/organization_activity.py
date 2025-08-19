from uuid import UUID

from app.models.organization import Organization
from app.repos.organization import OrganizationRepo
from app.schemas.organization_activity import OrganizationActivityResponseSchema
from app.services.base import SoftDeletableService


class OrganizationActivityService(
    SoftDeletableService[UUID, Organization, OrganizationActivityResponseSchema]
):
    response_schema = OrganizationActivityResponseSchema

    def __init__(self, repo: OrganizationRepo) -> None:
        super().__init__(repo)
        self.repo: OrganizationRepo = repo
