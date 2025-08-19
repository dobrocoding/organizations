from collections.abc import Sequence
from typing import Any

from app.resources import strings


def validate_exclusive_presence(first: Any | None, second: Any | None) -> None:
    """Validates that exactly one of `first` or `second` is provided.

    Raises a ValueError if none or both are provided.

    Args:
        first: The first value to check.
        second: The second value to check.

    """
    is_first = first is not None
    is_second = second is not None
    if is_first == is_second:  # Both are True or both are False
        raise ValueError(strings.EXCLUSIVE_PRESENCE)


def validate_excel_data(headers: Sequence[str], data: Sequence[Sequence[Any]]) -> None:
    """Validate that Excel headers and data have matching lengths.

    Args:
        headers: Sequence of column headers
        data: Sequence of rows, where each row is a sequence of values

    Raises:
        ValueError: If headers is empty or data rows don't match headers length

    """
    if not headers:
        raise ValueError(strings.EMPTY_HEADERS)

    headers_length = len(headers)

    for row_index, row in enumerate(data, start=1):
        row_length = len(row)
        if row_length != headers_length:
            error_message = (
                f'Row {row_index} has {row_length} columns, '
                f'but headers have {headers_length} columns'
            )
            raise ValueError(error_message)
