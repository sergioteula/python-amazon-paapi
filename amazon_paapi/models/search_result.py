from typing import List
from .item_result import Item
from ..sdk.models import SearchResult

class SearchResult(SearchResult):
    items: List[Item]
    total_result_count: int
    search_url: str
