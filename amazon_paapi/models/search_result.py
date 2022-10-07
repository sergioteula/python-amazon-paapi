from typing import List

from ..sdk.models import SearchResult
from .item_result import Item


class SearchResult(SearchResult):
    items: List[Item]
    total_result_count: int
    search_url: str
