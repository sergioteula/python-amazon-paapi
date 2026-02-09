"""Error handling utilities for the Amazon Creators API."""

from __future__ import annotations

from typing import NoReturn

from amazon_creatorsapi.core.constants import HTTP_NOT_FOUND, HTTP_TOO_MANY_REQUESTS
from amazon_creatorsapi.errors import (
    AssociateValidationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    TooManyRequestsError,
)


def handle_api_error(status_code: int, body: str) -> NoReturn:
    """Handle API error responses and raise appropriate exceptions.

    Args:
        status_code: HTTP status code.
        body: Response body text.

    Raises:
        ItemsNotFoundError: For 404 errors.
        TooManyRequestsError: For 429 errors.
        InvalidArgumentError: For validation errors.
        AssociateValidationError: For invalid associate credentials.
        RequestError: For other errors.

    """
    if status_code == HTTP_NOT_FOUND:
        msg = "No items found for the request"
        raise ItemsNotFoundError(msg)

    if status_code == HTTP_TOO_MANY_REQUESTS:
        msg = "Rate limit exceeded, try increasing throttling"
        raise TooManyRequestsError(msg)

    if "InvalidParameterValue" in body:
        msg = "Invalid parameter value provided in the request"
        raise InvalidArgumentError(msg)

    if "InvalidPartnerTag" in body:
        msg = "The partner tag is invalid or not present"
        raise InvalidArgumentError(msg)

    if "InvalidAssociate" in body:
        msg = "Credentials are not valid for the selected marketplace"
        raise AssociateValidationError(msg)

    # Generic error
    body_info = f" - {body[:200]}" if body else ""
    msg = f"Request failed with status {status_code}{body_info}"
    raise RequestError(msg)
