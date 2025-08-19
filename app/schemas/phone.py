from uuid import UUID

from app.schemas import AdminMeta, BaseResponseSchema


class BasePhoneResponseSchema(BaseResponseSchema):
    id: UUID
    number: str
    description: str | None
    is_primary: bool


class PhoneResponseSchema(BasePhoneResponseSchema, AdminMeta): ...
