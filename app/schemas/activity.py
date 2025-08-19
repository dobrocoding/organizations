from uuid import UUID

from pydantic import Field

from app.schemas.base import AdminMeta, BaseRequestSchema, BaseResponseSchema


class BaseActivityResponseSchema(BaseResponseSchema):
    id: UUID
    name: str
    description: str | None


class ActivityResponseSchema(BaseActivityResponseSchema, AdminMeta):
    parent: BaseActivityResponseSchema | None
    children: list[BaseActivityResponseSchema] | None


class CreateActivityRequestSchema(BaseRequestSchema):
    name: str = Field(max_length=255)
    description: str | None = None
    parent_id: UUID | None = None


class UpdateActivityRequestSchema(BaseRequestSchema):
    name: str | None = Field(max_length=255, default=None)
    description: str | None = None
    parent_id: UUID | None = None
