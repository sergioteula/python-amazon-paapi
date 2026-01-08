"""Module to manage items."""

from __future__ import annotations

from amazon_paapi import models


def sort_items(
    items: list[models.Item], items_ids: list[str], *, include_unavailable: bool
) -> list[models.Item]:
    """Sort items by the order of the provided items_ids list."""
    sorted_items: list[models.Item] = []

    for asin in items_ids:
        matches: list[models.Item] = [item for item in items if item.asin == asin]
        if matches:
            sorted_items.append(matches[0])
        elif include_unavailable:
            sorted_items.append(models.Item(asin=asin))

    return sorted_items
