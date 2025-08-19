from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING, Annotated, Union

from pydantic import PlainSerializer

if TYPE_CHECKING:
    from app.schemas.base import Filter, OrFilterGroup

AnyIPAddress = Annotated[IPv4Address | IPv6Address, PlainSerializer(str, return_type=str)]

Filters = Union['Filter', 'OrFilterGroup']
