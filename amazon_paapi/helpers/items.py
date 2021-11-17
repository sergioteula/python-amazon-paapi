"""Module to manage items"""

from typing import List
from .. import models


def get_items_including_unavailable(items: List[models.Item], items_ids: List[str]) -> List[models.Item]:
    for index, asin in enumerate(items_ids):
        if items[index].asin != asin:
            items.insert(index, models.Item(asin=asin))
    return items
