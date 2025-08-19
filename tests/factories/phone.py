from typing import Any
from uuid import UUID

from polyfactory import Use

from app.models.phone import Phone
from tests.factories.base import SQLAlchemyBaseModelFactory


class PhoneFactory(SQLAlchemyBaseModelFactory[Phone]):
    __model__ = Phone

    number = Use(lambda: PhoneFactory.__faker__.phone_number())  # noqa: PLW0108
    description = Use(lambda: PhoneFactory.__faker__.sentence())  # noqa: PLW0108
    is_primary = False

    @classmethod
    def build_with_organization(cls, organization_id: UUID, **kwargs: Any) -> Phone:
        return cls.build(organization_id=organization_id, **kwargs)

    @classmethod
    def build_primary(cls, organization_id: UUID, **kwargs: Any) -> Phone:
        return cls.build(organization_id=organization_id, is_primary=True, **kwargs)
