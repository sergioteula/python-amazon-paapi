"""Module to manage items"""

from typing import List
from .. import models


def sort_items(items: List[models.Item], items_ids: List[str], include_unavailable: bool) -> List[models.Item]:
    sorted_items = []

    for asin in items_ids:
        matches = list(filter(lambda item, asin=asin: item.asin == asin, items))
        if matches:
            sorted_items.append(matches[0])
        elif include_unavailable:
            sorted_items.append(models.Item(asin=asin))

    return sorted_items
