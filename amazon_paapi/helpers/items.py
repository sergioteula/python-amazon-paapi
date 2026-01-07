"""Module to manage items."""

from typing import List

from amazon_paapi import models


def sort_items(
    items: List[models.Item], items_ids: List[str], include_unavailable: bool
) -> List[models.Item]:
    """Sort items by the order of the provided items_ids list."""
    sorted_items: List[models.Item] = []

    for asin in items_ids:
        matches: List[models.Item] = [item for item in items if item.asin == asin]
        if matches:
            sorted_items.append(matches[0])
        elif include_unavailable:
            sorted_items.append(models.Item(asin=asin))

    return sorted_items
