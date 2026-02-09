"""Amazon Creators API wrapper for Python.

A Python wrapper for the Amazon Creators API.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, NoReturn

from amazon_creatorsapi.core.constants import DEFAULT_THROTTLING
from amazon_creatorsapi.core.error_handling import handle_api_error
from amazon_creatorsapi.core.parsers import get_asin, get_items_ids
from amazon_creatorsapi.core.resources import get_all_resources
from amazon_creatorsapi.core.validation import validate_and_get_marketplace
from amazon_creatorsapi.errors import ItemsNotFoundError
from creatorsapi_python_sdk.api.default_api import DefaultApi
from creatorsapi_python_sdk.api_client import ApiClient
from creatorsapi_python_sdk.exceptions import ApiException
from creatorsapi_python_sdk.models.get_browse_nodes_request_content import (
    GetBrowseNodesRequestContent,
)
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_items_request_content import (
    GetItemsRequestContent,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_variations_request_content import (
    GetVariationsRequestContent,
)
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.search_items_request_content import (
    SearchItemsRequestContent,
)
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode
    from creatorsapi_python_sdk.models.browse_node import BrowseNode
    from creatorsapi_python_sdk.models.condition import Condition
    from creatorsapi_python_sdk.models.item import Item
    from creatorsapi_python_sdk.models.search_result import SearchResult
    from creatorsapi_python_sdk.models.sort_by import SortBy
    from creatorsapi_python_sdk.models.variations_result import VariationsResult


class AmazonCreatorsApi:
    """Provides methods to get information from Amazon using the Creators API.

    Args:
        credential_id: Your Creators API credential ID.
        credential_secret: Your Creators API credential secret.
        version: API version for your region.
        tag: Your affiliate tracking id (partner tag).
        country: Country code (e.g., "ES", "US"). Used to determine marketplace.
        marketplace: Marketplace URL (e.g., "www.amazon.es"). Overrides country.
        throttling: Wait time in seconds between API calls. Defaults to 1 second.

    Raises:
        InvalidArgumentError: If neither country nor marketplace is provided.

    Example:
        >>> api = AmazonCreatorsApi(
        ...     credential_id="your_id",
        ...     credential_secret="your_secret",
        ...     version="2.2",
        ...     tag="your-tag",
        ...     country="ES"
        ... )
        >>> items = api.get_items(["B0DLFMFBJW"])

    """

    def __init__(
        self,
        credential_id: str,
        credential_secret: str,
        version: str,
        tag: str,
        country: CountryCode | None = None,
        marketplace: str | None = None,
        throttling: float = DEFAULT_THROTTLING,
    ) -> None:
        """Initialize the Amazon Creators API client."""
        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self._last_query_time = time.time() - throttling
        self.tag = tag
        self.throttling = float(throttling)

        # Determine marketplace from country or direct value
        self.marketplace = validate_and_get_marketplace(country, marketplace)

        self._api_client = ApiClient(
            credential_id=credential_id,
            credential_secret=credential_secret,
            version=version,
        )
        self._api = DefaultApi(self._api_client)

    def get_items(
        self,
        items: str | list[str],
        condition: Condition | None = None,
        currency_of_preference: str | None = None,
        languages_of_preference: list[str] | None = None,
        resources: list[GetItemsResource] | None = None,
    ) -> list[Item]:
        """Get items information from Amazon.

        Args:
            items: One or more items, using ASIN or Amazon product URL.
                Accepts a single string (comma-separated) or a list of strings.
            condition: Filter offers by condition type.
            currency_of_preference: ISO 4217 currency code for prices.
            languages_of_preference: Languages in order of preference.
            resources: List of resources to retrieve. Defaults to all.

        Returns:
            List of Item objects with Amazon information.

        Raises:
            ItemsNotFoundError: If no items are found.
            InvalidArgumentError: If parameters are invalid.

        """
        if resources is None:
            resources = get_all_resources(GetItemsResource)

        item_ids = get_items_ids(items)

        request = GetItemsRequestContent(
            partnerTag=self.tag,
            itemIds=item_ids,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        self._throttle()

        try:
            response = self._api.get_items(
                x_marketplace=self.marketplace,
                get_items_request_content=request,
            )
        except ApiException as exc:
            self._handle_api_exception(exc)

        if response.items_result is None or response.items_result.items is None:
            msg = "No items have been found"
            raise ItemsNotFoundError(msg)

        return response.items_result.items

    def search_items(
        self,
        keywords: str | None = None,
        actor: str | None = None,
        artist: str | None = None,
        author: str | None = None,
        brand: str | None = None,
        title: str | None = None,
        browse_node_id: str | None = None,
        search_index: str | None = None,
        item_count: int | None = None,
        item_page: int | None = None,
        condition: Condition | None = None,
        currency_of_preference: str | None = None,
        languages_of_preference: list[str] | None = None,
        max_price: int | None = None,
        min_price: int | None = None,
        min_saving_percent: int | None = None,
        min_reviews_rating: int | None = None,
        sort_by: SortBy | None = None,
        resources: list[SearchItemsResource] | None = None,
    ) -> SearchResult:
        """Search for items on Amazon based on a search query.

        At least one of the following parameters should be specified: keywords,
        actor, artist, author, brand, title, browse_node_id or search_index.

        Args:
            keywords: A word or phrase that describes an item.
            actor: Actor name associated with the item.
            artist: Artist name associated with the item.
            author: Author name associated with the item.
            brand: Brand name associated with the item.
            title: Title associated with the item.
            browse_node_id: A unique ID for a product category.
            search_index: Product category to search. Defaults to All.
            item_count: Number of items returned (1-10). Defaults to 10.
            item_page: Page of items to return (1-10). Defaults to 1.
            condition: Filter offers by condition type.
            currency_of_preference: ISO 4217 currency code for prices.
            languages_of_preference: Languages in order of preference.
            max_price: Max price in lowest currency denomination.
            min_price: Min price in lowest currency denomination.
            min_saving_percent: Min savings percentage (1-99).
            min_reviews_rating: Min review rating (1-5).
            sort_by: Sort method for results.
            resources: List of resources to retrieve. Defaults to all.

        Returns:
            SearchResult containing the list of items.

        Raises:
            ItemsNotFoundError: If no items are found.

        """
        if resources is None:
            resources = get_all_resources(SearchItemsResource)

        request = SearchItemsRequestContent(
            partnerTag=self.tag,
            keywords=keywords,
            actor=actor,
            artist=artist,
            author=author,
            brand=brand,
            title=title,
            browseNodeId=browse_node_id,
            searchIndex=search_index,
            itemCount=item_count,
            itemPage=item_page,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            languagesOfPreference=languages_of_preference,
            maxPrice=max_price,
            minPrice=min_price,
            minSavingPercent=min_saving_percent,
            minReviewsRating=min_reviews_rating,
            sortBy=sort_by,
            resources=resources,
        )

        self._throttle()

        try:
            response = self._api.search_items(
                x_marketplace=self.marketplace,
                search_items_request_content=request,
            )
        except ApiException as exc:
            self._handle_api_exception(exc)

        if response.search_result is None:
            msg = "No items have been found"
            raise ItemsNotFoundError(msg)

        return response.search_result

    def get_variations(
        self,
        asin: str,
        variation_count: int | None = None,
        variation_page: int | None = None,
        condition: Condition | None = None,
        currency_of_preference: str | None = None,
        languages_of_preference: list[str] | None = None,
        resources: list[GetVariationsResource] | None = None,
    ) -> VariationsResult:
        """Return variations of a product (different sizes, colors, etc.).

        Args:
            asin: The ASIN or Amazon product URL of the product.
            variation_count: Number of variations to return (1-10). Defaults to 10.
            variation_page: Page of variations to return (1-10). Defaults to 1.
            condition: Filter offers by condition type.
            currency_of_preference: ISO 4217 currency code for prices.
            languages_of_preference: Languages in order of preference.
            resources: List of resources to retrieve. Defaults to all.

        Returns:
            VariationsResult containing the list of variations.

        Raises:
            ItemsNotFoundError: If no variations are found.

        """
        if resources is None:
            resources = get_all_resources(GetVariationsResource)

        asin = get_asin(asin)

        request = GetVariationsRequestContent(
            partnerTag=self.tag,
            asin=asin,
            variationCount=variation_count,
            variationPage=variation_page,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        self._throttle()

        try:
            response = self._api.get_variations(
                x_marketplace=self.marketplace,
                get_variations_request_content=request,
            )
        except ApiException as exc:
            self._handle_api_exception(exc)

        if response.variations_result is None:
            msg = "No variations have been found"
            raise ItemsNotFoundError(msg)

        return response.variations_result

    def get_browse_nodes(
        self,
        browse_node_ids: list[str],
        languages_of_preference: list[str] | None = None,
        resources: list[GetBrowseNodesResource] | None = None,
    ) -> list[BrowseNode]:
        """Return browse node information including name, children, and ancestors.

        Args:
            browse_node_ids: List of browse node IDs.
            languages_of_preference: Languages in order of preference.
            resources: List of resources to retrieve. Defaults to all.

        Returns:
            List of BrowseNode objects.

        Raises:
            ItemsNotFoundError: If no browse nodes are found.

        """
        if resources is None:
            resources = get_all_resources(GetBrowseNodesResource)

        request = GetBrowseNodesRequestContent(
            partnerTag=self.tag,
            browseNodeIds=browse_node_ids,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        self._throttle()

        try:
            response = self._api.get_browse_nodes(
                x_marketplace=self.marketplace,
                get_browse_nodes_request_content=request,
            )
        except ApiException as exc:
            self._handle_api_exception(exc)

        if (
            response.browse_nodes_result is None
            or response.browse_nodes_result.browse_nodes is None
        ):
            msg = "No browse nodes have been found"
            raise ItemsNotFoundError(msg)

        return response.browse_nodes_result.browse_nodes

    def _throttle(self) -> None:
        """Wait for the throttling interval to elapse since the last API call."""
        wait_time = self.throttling - (time.time() - self._last_query_time)
        if wait_time > 0:
            time.sleep(wait_time)
        self._last_query_time = time.time()

    def _handle_api_exception(self, error: ApiException) -> NoReturn:
        """Handle API exceptions and raise appropriate custom exceptions."""
        error_body = str(error.body) if error.body else ""
        try:
            handle_api_error(error.status, error_body)
        except Exception as exc:
            # Re-raise with original exception as cause for better stack traces
            raise exc from error
