"""Module with helper functions for managing arguments."""

from typing import List, Union

from amazon_paapi.errors import InvalidArgument
from amazon_paapi.tools import get_asin


def get_items_ids(items: Union[str, List[str]]) -> List[str]:
    """Parse and extract ASINs from items input.

    Args:
        items: Either a comma-separated string of ASINs/URLs or a list of ASINs/URLs.

    Returns:
        A list of extracted ASINs.

    Raises:
        InvalidArgument: If items is not a string or list.

    """
    if isinstance(items, str):
        items_ids = items.split(",")
        return [get_asin(x.strip()) for x in items_ids]

    if isinstance(items, list):
        return [get_asin(x.strip()) for x in items]

    msg = "Invalid items argument, it should be a string or List of strings"  # type: ignore[unreachable]
    raise InvalidArgument(msg)


def check_search_args(**kwargs) -> None:
    """Validate all search arguments."""
    check_search_mandatory_args(**kwargs)
    check_search_pagination_args(**kwargs)


def check_search_mandatory_args(**kwargs) -> None:
    """Validate that at least one mandatory search argument is provided."""
    mandatory_args = [
        kwargs.get("keywords"),
        kwargs.get("actor"),
        kwargs.get("artist"),
        kwargs.get("author"),
        kwargs.get("brand"),
        kwargs.get("title"),
        kwargs.get("browse_node_id"),
        kwargs.get("search_index"),
    ]
    if all(arg is None for arg in mandatory_args):
        error_message = (
            "At least one of the following args should be provided: keywords, actor,"
            " artist, author, brand, title, browse_node_id or search_index."
        )
        raise InvalidArgument(error_message)


def check_search_pagination_args(**kwargs) -> None:
    """Validate pagination arguments for search requests."""
    error_message = "Args item_count and item_page should be integers between 1 and 10."
    pagination_args = [kwargs.get("item_count"), kwargs.get("item_page")]

    for arg in pagination_args:
        if arg is not None and (not isinstance(arg, int) or not 1 <= arg <= 10):
            raise InvalidArgument(error_message)


def check_variations_args(**kwargs) -> None:
    """Validate variation arguments for get_variations requests."""
    error_message = (
        "Args variation_count and variation_page should be integers between 1 and 10."
    )
    variation_args = [kwargs.get("variation_count"), kwargs.get("variation_page")]

    for arg in variation_args:
        if arg is not None and (not isinstance(arg, int) or not 1 <= arg <= 10):
            raise InvalidArgument(error_message)


def check_browse_nodes_args(**kwargs) -> None:
    """Validate browse node arguments."""
    if not isinstance(kwargs.get("browse_node_ids"), List):
        error_message = "Argument browse_node_ids should be a List of strings."
        raise InvalidArgument(error_message)
