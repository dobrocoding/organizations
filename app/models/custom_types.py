from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import mapped_column

str_20 = Annotated[str, mapped_column(String(20))]
str_36 = Annotated[str, mapped_column(String(36))]
str_255 = Annotated[str, mapped_column(String(255))]
str_255_or_none = Annotated[str | None, mapped_column(String(255), nullable=True, default=None)]
