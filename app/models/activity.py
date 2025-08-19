from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.custom_types import str_255

if TYPE_CHECKING:
    from app.models.organization import Organization


class Activity(BaseModel):
    name: Mapped[str_255]
    description: Mapped[str | None]

    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey('activity.id'), nullable=True)

    parent: Mapped['Activity | None'] = relationship(
        'Activity', remote_side='Activity.id', foreign_keys=[parent_id], back_populates='children'
    )
    children: Mapped[list['Activity']] = relationship(
        'Activity', foreign_keys=[parent_id], back_populates='parent', cascade='all, delete-orphan'
    )

    organizations: Mapped[list['Organization']] = relationship(
        'Organization', secondary='organization_activity', back_populates='activities'
    )
