"""Utilities to prepare and order the items of a request."""

from __future__ import annotations

from typing import TYPE_CHECKING

from amazon_creatorsapi.core.constants import MAX_ITEMS_PER_REQUEST
from creatorsapi_python_sdk.models.item import Item

if TYPE_CHECKING:
    from collections.abc import Iterator


def get_unique_items(item_ids: list[str]) -> list[str]:
    """Remove duplicated identifiers, keeping the order of the original list.

    Args:
        item_ids: List of item identifiers, possibly with duplicates.

    Returns:
        The identifiers without duplicates, in their original order.

    """
    return list(dict.fromkeys(item_ids))


def get_item_chunks(item_ids: list[str]) -> Iterator[list[str]]:
    """Split the identifiers into chunks of the size accepted by Amazon.

    Args:
        item_ids: List of item identifiers.

    Yields:
        Chunks of identifiers, none of them above the API limit.

    """
    for index in range(0, len(item_ids), MAX_ITEMS_PER_REQUEST):
        yield item_ids[index : index + MAX_ITEMS_PER_REQUEST]


def sort_items(
    items: list[Item],
    item_ids: list[str],
    *,
    include_unavailable: bool,
) -> list[Item]:
    """Sort the items following the order of the requested identifiers.

    Args:
        items: Items returned by Amazon, in any order.
        item_ids: Requested identifiers, in the order they were asked for.
        include_unavailable: Add an item holding only the ASIN for every
            identifier missing from the response.

    Returns:
        The items in the order of the requested identifiers.

    """
    items_by_asin = {item.asin: item for item in items if item.asin is not None}
    sorted_items: list[Item] = []

    for asin in item_ids:
        item = items_by_asin.get(asin)
        if item is not None:
            sorted_items.append(item)
        elif include_unavailable:
            sorted_items.append(Item(asin=asin))

    return sorted_items
