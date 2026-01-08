"""Search result model for Amazon Product Advertising API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from amazon_paapi.sdk import models as sdk_models

if TYPE_CHECKING:
    from .item_result import Item


class SearchResult(sdk_models.SearchResult):
    """Represent the result of a search operation."""

    items: list[Item]
    total_result_count: int
    search_url: str
