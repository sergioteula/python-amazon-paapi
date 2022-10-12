from typing import List

from ..sdk import models as sdk_models
from .item_result import Item


class SearchResult(sdk_models.SearchResult):
    items: List[Item]
    total_result_count: int
    search_url: str
