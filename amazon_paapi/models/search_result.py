"""Search result model for Amazon Product Advertising API."""

from typing import List

from amazon_paapi.sdk import models as sdk_models

from .item_result import Item


class SearchResult(sdk_models.SearchResult):
    """Represent the result of a search operation."""

    items: List[Item]
    total_result_count: int
    search_url: str
