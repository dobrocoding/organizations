from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from sqlalchemy.orm import joinedload

from app.models.activity import Activity
from app.repos.base import SoftDeletableRepo

if TYPE_CHECKING:
    pass


class ActivityRepo(SoftDeletableRepo[UUID, Activity]):
    load_options: ClassVar[list[Any]] = [
        joinedload(Activity.children),
        joinedload(Activity.organizations),
    ]
