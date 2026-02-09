"""Validation utilities for the Amazon Creators API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from amazon_creatorsapi.core.marketplaces import MARKETPLACES
from amazon_creatorsapi.errors import InvalidArgumentError

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode


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
