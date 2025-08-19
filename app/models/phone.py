from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.custom_types import str_20, str_255_or_none

if TYPE_CHECKING:
    from app.models.organization import Organization


class Phone(BaseModel):
    number: Mapped[str_20]
    organization_id: Mapped[UUID] = mapped_column(ForeignKey('organization.id'), nullable=False)

    description: Mapped[str_255_or_none]
    is_primary: Mapped[bool] = mapped_column(default=False)

    organization: Mapped['Organization'] = relationship('Organization', back_populates='phones')
