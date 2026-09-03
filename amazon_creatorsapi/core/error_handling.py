"""Error handling utilities for the Amazon Creators API."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, NoReturn

from amazon_creatorsapi.core.constants import (
    HTTP_BAD_REQUEST,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
    HTTP_TOO_MANY_REQUESTS,
    HTTP_UNAUTHORIZED,
)
from amazon_creatorsapi.errors import (
    AccessDeniedError,
    AmazonCreatorsApiError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    TooManyRequestsError,
)

if TYPE_CHECKING:
    from creatorsapi_python_sdk.models.error_data import ErrorData

# Reason returned by the API when the associate is not valid for the marketplace
INVALID_ASSOCIATE_REASON = "InvalidAssociate"

# Amount of characters of the response body kept for unexpected errors
MAX_BODY_LENGTH = 200


def parse_error_body(body: str) -> dict[str, Any]:
    """Parse the body of an error response.

    Args:
        body: Response body text.

    Returns:
        The parsed body, or an empty dictionary when it is not a JSON object.

    """
    try:
        data = json.loads(body)
    except (TypeError, ValueError):
        return {}

    return data if isinstance(data, dict) else {}


def get_error_detail(data: dict[str, Any], body: str) -> str:
    """Build a readable detail from the contents of an error response.

    Args:
        data: Parsed body of the error response.
        body: Original response body text.

    Returns:
        The details of the error as text, empty when there are none.

    """
    parts = [str(value) for value in (data.get("reason"), data.get("message")) if value]

    parts.extend(
        f"{field.get('name')}: {field.get('message')}"
        for field in data.get("fieldList") or []
        if isinstance(field, dict)
    )

    parts.extend(
        f"{name}: {data[name]}"
        for name in ("resourceType", "resourceId")
        if data.get(name)
    )

    if not parts and body:
        parts.append(body[:MAX_BODY_LENGTH])

    return f" - {'; '.join(parts)}" if parts else ""


def handle_api_error(
    status_code: int,
    body: str,
    not_found_error: type[AmazonCreatorsApiError] = ItemsNotFoundError,
) -> NoReturn:
    """Handle API error responses and raise appropriate exceptions.

    Args:
        status_code: HTTP status code.
        body: Response body text.
        not_found_error: Exception raised for a missing resource, so that
            operations tell apart items from feeds and reports.

    Raises:
        InvalidArgumentError: For requests rejected by the API.
        AssociateValidationError: For invalid associate credentials.
        AuthenticationError: For missing or invalid credentials.
        AccessDeniedError: For credentials without access to the operation.
        ItemsNotFoundError: For missing items, unless another error is given.
        TooManyRequestsError: For throttled requests.
        RequestError: For any other error.

    """
    data = parse_error_body(body)
    detail = get_error_detail(data, body)
    reason = data.get("reason")

    if status_code == HTTP_BAD_REQUEST:
        if reason == INVALID_ASSOCIATE_REASON or (
            reason is None and INVALID_ASSOCIATE_REASON in body
        ):
            msg = f"Credentials are not valid for the selected marketplace{detail}"
            raise AssociateValidationError(msg)
        msg = f"The request was rejected by Amazon{detail}"
        raise InvalidArgumentError(msg)

    if status_code == HTTP_UNAUTHORIZED:
        msg = f"Authentication failed{detail}"
        raise AuthenticationError(msg)

    if status_code == HTTP_FORBIDDEN:
        msg = f"Access denied for the requested operation{detail}"
        raise AccessDeniedError(msg)

    if status_code == HTTP_NOT_FOUND:
        msg = f"No results found for the request{detail}"
        raise not_found_error(msg)

    if status_code == HTTP_TOO_MANY_REQUESTS:
        msg = f"Rate limit exceeded, try increasing throttling{detail}"
        raise TooManyRequestsError(msg)

    msg = f"Request failed with status {status_code}{detail}"
    raise RequestError(msg)


def format_errors(errors: list[ErrorData] | None) -> str:
    """Return a readable summary of the partial errors of a response.

    Args:
        errors: Partial errors returned by the API, if any.

    Returns:
        The errors as text, or an empty string when there are none.

    """
    if not errors:
        return ""
    details = "; ".join(f"{error.code}: {error.message}" for error in errors)
    return f" ({details})"
