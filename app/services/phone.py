from typing import TYPE_CHECKING
from uuid import UUID

from app.models.phone import Phone
from app.repos.phone import PhoneRepo
from app.schemas import PhoneResponseSchema
from app.services.base import SoftDeletableService

if TYPE_CHECKING:
    pass


class PhoneService(SoftDeletableService[UUID, Phone, PhoneResponseSchema]):
    response_schema = PhoneResponseSchema

    def __init__(self, repo: PhoneRepo) -> None:
        super().__init__(repo)
        self.repo: PhoneRepo = repo
