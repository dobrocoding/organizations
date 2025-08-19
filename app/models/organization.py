from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.custom_types import str_255, str_255_or_none

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.building import Building
    from app.models.phone import Phone


class Organization(BaseModel):
    name: Mapped[str_255]
    building_id: Mapped[UUID] = mapped_column(ForeignKey('building.id'), nullable=False)
    description: Mapped[str | None]
    website: Mapped[str_255_or_none]
    email: Mapped[str_255_or_none]

    building: Mapped['Building'] = relationship('Building', back_populates='organizations')

    phones: Mapped[list['Phone']] = relationship(
        'Phone', back_populates='organization', cascade='all, delete-orphan'
    )

    activities: Mapped[list['Activity']] = relationship(
        'Activity', secondary='organization_activity', back_populates='organizations'
    )
