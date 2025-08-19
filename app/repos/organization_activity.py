from uuid import UUID

from app.models import OrganizationActivity
from app.repos import SoftDeletableRepo


class OrganizationActivityRepo(SoftDeletableRepo[UUID, OrganizationActivity]): ...
