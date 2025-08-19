import re
import typing
from collections.abc import Sequence
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.types import AnyIPAddress
from app.resources.enums.order_by import OrderByDirections


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CreateUpdateMeta(BaseModel):
    created_at: datetime
    updated_at: datetime


class AdminMeta(CreateUpdateMeta):
    deleted_at: datetime | None = None


class AdminResponseSchema(BaseResponseSchema):
    id: UUID
    full_name: str | None = None
    unovay_name: str | None = None


class PaginationMetaSchema(BaseModel):
    limit: int
    total: int
    current_page: int
    last_page: int


class PaginatedResponseSchema[T](BaseResponseSchema):
    meta: PaginationMetaSchema
    data: Sequence[T]


class ClientMeta(BaseRequestSchema):
    ip_address: AnyIPAddress | None = None
    user_agent: str | None = None


class OrderBy(BaseModel):
    field: str
    direction: OrderByDirections


class BaseOrderBySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def build_order_by(self) -> list[OrderBy]:
        data = self.model_dump(exclude_unset=True, exclude_none=True)
        return [OrderBy(field=k, direction=v) for k, v in data.items()]


FilterOp = Literal[
    'eq', '=', 'ilike', '~=', 'is', 'is_not', 'in', 'gt', '>', 'ge', '>=', 'lt', '<', 'le', '<='
]
filter_op_values = typing.get_args(FilterOp)


class Filter(BaseModel):
    field: str
    op: FilterOp = '='
    value: Any | None


class OrFilterGroup(BaseModel):
    filters: list[Filter]


class BaseFiltersSchema(BaseModel):
    def build_filters(self, *, exclude: set[str] | None = None) -> list[Filter]:
        fields_data = self.model_dump(
            exclude_unset=True, exclude_none=True, exclude=exclude or set()
        )
        filters = []
        for k, v in fields_data.items():
            op: FilterOp
            if suffix := re.search(r'__(\w+)$', k):
                parsed_op = suffix.group(1)
                if parsed_op not in filter_op_values:
                    raise ValueError
                field_name = k[: -len(suffix.group(0))]
                op = typing.cast(FilterOp, parsed_op)
            else:
                field_name = k
                op = '='
            filters.append(Filter(field=field_name, op=op, value=v))

        return filters

    model_config = ConfigDict(from_attributes=True)
