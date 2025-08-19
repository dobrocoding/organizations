from typing import Any

from polyfactory import Use

from app.models.activity import Activity
from tests.factories.base import SQLAlchemyBaseModelFactory


class ActivityFactory(SQLAlchemyBaseModelFactory[Activity]):
    __model__ = Activity

    name = Use(lambda: f'Activity {ActivityFactory.__faker__.word().title()}')
    description = Use(lambda: ActivityFactory.__faker__.sentence())  # noqa: PLW0108
    parent_id = None

    @classmethod
    def build_with_parent(cls, parent: Activity, **kwargs: Any) -> Activity:
        return cls.build(parent_id=parent.id, **kwargs)

    @classmethod
    def build_root(cls, **kwargs: Any) -> Activity:
        return cls.build(parent_id=None, **kwargs)
