from typing import TYPE_CHECKING
from uuid import UUID

from app.models.phone import Phone
from app.repos.base import SoftDeletableRepo

if TYPE_CHECKING:
    pass


class PhoneRepo(SoftDeletableRepo[UUID, Phone]): ...
