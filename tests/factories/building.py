from decimal import Decimal
from typing import Any

from polyfactory import Use

from app.models.building import Building
from tests.factories.base import SQLAlchemyBaseModelFactory


class BuildingFactory(SQLAlchemyBaseModelFactory[Building]):
    __model__ = Building

    address = Use(
        lambda: f'{BuildingFactory.__faker__.street_address()}, {BuildingFactory.__faker__.city()}'
    )
    latitude = Use(lambda: Decimal(str(BuildingFactory.__faker__.latitude())))
    longitude = Use(lambda: Decimal(str(BuildingFactory.__faker__.longitude())))
    name = Use(lambda: f'Building {BuildingFactory.__faker__.word().title()}')
    description = Use(lambda: BuildingFactory.__faker__.sentence())  # noqa: PLW0108

    @classmethod
    def build_in_moscow(cls, **kwargs: Any) -> Building:
        return cls.build(latitude=Decimal('55.7558'), longitude=Decimal('37.6176'), **kwargs)
