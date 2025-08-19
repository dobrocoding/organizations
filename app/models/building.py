from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.custom_types import str_255_or_none

if TYPE_CHECKING:
    from app.models.organization import Organization


class Building(BaseModel):
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[Decimal]
    longitude: Mapped[Decimal]
    name: Mapped[str_255_or_none]
    description: Mapped[str | None]
    organizations: Mapped[list['Organization']] = relationship(
        'Organization', back_populates='building'
    )
