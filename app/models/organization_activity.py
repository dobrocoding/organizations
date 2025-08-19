from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class OrganizationActivity(BaseModel):
    organization_id: Mapped[UUID] = mapped_column(ForeignKey('organization.id'), primary_key=True)
    activity_id: Mapped[UUID] = mapped_column(ForeignKey('activity.id'), primary_key=True)
