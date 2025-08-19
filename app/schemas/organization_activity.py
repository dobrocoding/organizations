from app.schemas import (
    AdminMeta,
    BaseActivityResponseSchema,
    BaseOrganizationResponseSchema,
    BaseResponseSchema,
)


class BaseOrganizationActivityResponseSchema(BaseResponseSchema):
    organization: BaseOrganizationResponseSchema
    activity: BaseActivityResponseSchema


class OrganizationActivityResponseSchema(BaseOrganizationActivityResponseSchema, AdminMeta): ...
