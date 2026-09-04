"""Validation utilities for the Amazon Creators API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel, ValidationError

from amazon_creatorsapi.core.marketplaces import MARKETPLACES
from amazon_creatorsapi.errors import InvalidArgumentError

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode

RequestT = TypeVar("RequestT", bound=BaseModel)


def validate_and_get_marketplace(
    country: CountryCode | None,
    marketplace: str | None,
) -> str:
    """Validate and determine marketplace from country or direct value.

    Args:
        country: Country code (e.g., "ES", "US").
        marketplace: Marketplace URL (e.g., "www.amazon.es").

    Returns:
        The marketplace URL.

    Raises:
        InvalidArgumentError: If neither country nor marketplace is provided,
            or if the country code is invalid.

    """
    if marketplace:
        return marketplace
    if country:
        if country not in MARKETPLACES:
            msg = f"Country code '{country}' is not valid"
            raise InvalidArgumentError(msg)
        return MARKETPLACES[country]
    msg = "Either 'country' or 'marketplace' must be provided"
    raise InvalidArgumentError(msg)


def validate_timeout(timeout: float | None) -> float | None:
    """Validate the request timeout value.

    Args:
        timeout: Request timeout in seconds, or None to wait indefinitely.

    Returns:
        The timeout as a float, or None when disabled.

    Raises:
        InvalidArgumentError: If the timeout is not greater than zero.

    """
    if timeout is None:
        return None
    try:
        value = float(timeout)
    except (TypeError, ValueError) as error:
        msg = f"Timeout must be a number of seconds, or None: {timeout!r}"
        raise InvalidArgumentError(msg) from error
    if value <= 0:
        msg = "Timeout must be greater than zero, or None to wait indefinitely"
        raise InvalidArgumentError(msg)
    return value


def validate_throttling(throttling: float) -> float:
    """Validate the wait time between API calls.

    Args:
        throttling: Wait time in seconds between API calls.

    Returns:
        The wait time as a float.

    Raises:
        InvalidArgumentError: If the wait time is not a number or is negative.

    """
    try:
        value = float(throttling)
    except (TypeError, ValueError) as error:
        msg = f"Throttling must be a number of seconds: {throttling!r}"
        raise InvalidArgumentError(msg) from error
    if value < 0:
        msg = "Throttling must be zero or greater"
        raise InvalidArgumentError(msg)
    return value


def build_request(request_class: type[RequestT], **fields: Any) -> RequestT:
    """Build a request for the SDK, validating the values it receives.

    Args:
        request_class: Request model from the SDK.
        fields: Values for the request, using the names of the API.

    Returns:
        The request model filled with the provided values.

    Raises:
        InvalidArgumentError: If any value is rejected by the API constraints.

    """
    try:
        return request_class(**fields)
    except ValidationError as error:
        details = "; ".join(
            f"{'.'.join(str(location) for location in issue['loc'])}: {issue['msg']}"
            for issue in error.errors()
        )
        msg = f"Invalid parameters for the request: {details}"
        raise InvalidArgumentError(msg) from error


def validate_retries(retries: int) -> int:
    """Validate the amount of retries for a failed request.

    Args:
        retries: Amount of extra attempts for a failure that can be retried.

    Returns:
        The amount of retries as an integer.

    Raises:
        InvalidArgumentError: If the amount of retries is not a whole number
            or is negative.

    """
    try:
        value = int(retries)
    except (TypeError, ValueError) as error:
        msg = f"Retries must be a whole number: {retries!r}"
        raise InvalidArgumentError(msg) from error
    if value < 0:
        msg = "Retries must be zero or greater"
        raise InvalidArgumentError(msg)
    return value


def validate_search_criteria(**criteria: object) -> None:
    """Validate that a search has at least one criterion to look for.

    Args:
        criteria: Arguments of the search, by name.

    Raises:
        InvalidArgumentError: If every criterion is missing.

    """
    if all(value is None for value in criteria.values()):
        names = ", ".join(criteria)
        msg = f"At least one of these arguments is required: {names}"
        raise InvalidArgumentError(msg)
