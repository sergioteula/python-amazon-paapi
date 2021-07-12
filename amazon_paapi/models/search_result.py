from .api_item import Item
from ..sdk.models import SearchResult

class SearchResult(SearchResult):
    items: list[Item]
    total_result_count: int
    search_url: str
