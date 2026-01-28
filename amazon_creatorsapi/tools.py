"""Tools for extracting ASINs from URLs and text."""

from __future__ import annotations

import re

from amazon_creatorsapi.errors import InvalidArgumentError


def get_asin(text: str) -> str:
    """Extract the ASIN from a given text or URL.

    Args:
        text: A string containing an ASIN or Amazon product URL.

    Returns:
        The extracted ASIN in uppercase.

    Raises:
        InvalidArgumentError: If no valid ASIN can be found in the text.

    """
    # Return if text is already an ASIN (10 alphanumeric characters)
    if re.search(r"^[a-zA-Z0-9]{10}$", text):
        return text.upper()

    # Extract ASIN from URL searching for common Amazon URL patterns
    asin = re.search(r"(dp|gp/product|gp/aw/d|dp/product)/([a-zA-Z0-9]{10})", text)
    if asin:
        return asin.group(2).upper()

    msg = f"ASIN not found in: {text}"
    raise InvalidArgumentError(msg)


def get_items_ids(items: str | list[str]) -> list[str]:
    """Parse and extract ASINs from items input.

    Args:
        items: Either a comma-separated string of ASINs/URLs or a list of ASINs/URLs.

    Returns:
        A list of extracted ASINs.

    Raises:
        InvalidArgumentError: If items is not a string or list.

    """
    if isinstance(items, str):
        items = items.split(",")

    return [get_asin(x.strip()) for x in items]
