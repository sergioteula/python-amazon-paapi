"""Utilities to retry the requests that Amazon asks to retry."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

# Amount of extra attempts made for a failure that can be retried
DEFAULT_RETRIES = 3

# Seconds waited before the first retry, doubled on every following one
BACKOFF_FACTOR = 1.0
MAX_BACKOFF = 30.0

# Status codes that Amazon asks to retry with exponential backoff
RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

RETRY_AFTER_HEADER = "retry-after"


def is_retryable(status_code: int | None) -> bool:
    """Return whether a status code is worth retrying.

    Args:
        status_code: Status code of the response, if there is one.

    Returns:
        True when the request can be retried, False otherwise.

    """
    return status_code in RETRY_STATUS_CODES


def get_retry_after(headers: Mapping[str, str] | None) -> float | None:
    """Return the seconds requested by the Retry-After header, if any.

    Args:
        headers: Headers of the response.

    Returns:
        The amount of seconds to wait, or None when the header is missing or
        holds neither an amount of seconds nor a date.

    """
    if not headers:
        return None

    for name, value in headers.items():
        if name.lower() != RETRY_AFTER_HEADER:
            continue
        try:
            return max(float(value), 0.0)
        except (TypeError, ValueError):
            return get_seconds_until(value)

    return None


def get_seconds_until(value: str) -> float | None:
    """Return the seconds left until an HTTP date, which Retry-After allows.

    Args:
        value: Value of the header, expected to hold a date.

    Returns:
        The amount of seconds until the date, zero when it is already past,
        or None when the value is not a date.

    """
    # Python 3.9 reports an unparseable value with a TypeError instead of the
    # ValueError raised by the newer versions
    try:
        date = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    return max((date - datetime.now(timezone.utc)).total_seconds(), 0.0)


def get_retry_delay(attempt: int, headers: Mapping[str, str] | None = None) -> float:
    """Return the seconds to wait before the next attempt.

    Args:
        attempt: Amount of retries already made for the request.
        headers: Headers of the response, used to honour Retry-After.

    Returns:
        The amount of seconds to wait, never above the maximum backoff.

    """
    retry_after = get_retry_after(headers)
    if retry_after is not None:
        return min(retry_after, MAX_BACKOFF)

    return min(BACKOFF_FACTOR * 2.0**attempt, MAX_BACKOFF)
