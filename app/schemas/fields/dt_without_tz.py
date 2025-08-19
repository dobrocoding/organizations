from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer


def datetime_encoder(dec_value: datetime) -> datetime:
    return dec_value.replace(tzinfo=None)


dt_without_tz = Annotated[
    datetime,
    AfterValidator(datetime_encoder),
    PlainSerializer(datetime_encoder, return_type=datetime),
]
