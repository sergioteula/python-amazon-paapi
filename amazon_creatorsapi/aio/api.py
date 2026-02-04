"""Async Amazon Creators API wrapper for Python.

Provides async methods to interact with the Amazon Creators API.
"""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from amazon_creatorsapi.core.constants import DEFAULT_THROTTLING
from amazon_creatorsapi.core.marketplaces import MARKETPLACES
from amazon_creatorsapi.core.parsers import get_asin, get_items_ids
from amazon_creatorsapi.errors import (
    AssociateValidationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    TooManyRequestsError,
)

try:
    from .auth import AsyncOAuth2TokenManager
    from .client import AsyncHttpClient
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc

from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource

if TYPE_CHECKING:
    from enum import Enum
    from types import TracebackType

    from amazon_creatorsapi.core.marketplaces import CountryCode
    from creatorsapi_python_sdk.models.condition import Condition
    from creatorsapi_python_sdk.models.sort_by import SortBy

from creatorsapi_python_sdk.models.browse_node import BrowseNode
from creatorsapi_python_sdk.models.item import Item
from creatorsapi_python_sdk.models.search_result import SearchResult
from creatorsapi_python_sdk.models.variations_result import VariationsResult

# API endpoints
API_HOST = "https://creatorsapi.amazon"
ENDPOINT_GET_ITEMS = "/catalog/v1/getItems"
ENDPOINT_SEARCH_ITEMS = "/catalog/v1/searchItems"
ENDPOINT_GET_VARIATIONS = "/catalog/v1/getVariations"
ENDPOINT_GET_BROWSE_NODES = "/catalog/v1/getBrowseNodes"


class AsyncAmazonCreatorsApi:
    """Async version of Amazon Creators API wrapper.

    Provides async methods to get information from Amazon using the Creators API.
    This class can be used with or without a context manager.

    Basic usage (creates new HTTP connection per request):
        >>> api = AsyncAmazonCreatorsApi(
        ...     credential_id="your_id",
        ...     credential_secret="your_secret",
        ...     version="2.2",
        ...     tag="your-tag",
        ...     country="ES"
        ... )
        >>> items = await api.get_items(["B0DLFMFBJW"])

    Advanced usage with context manager (reuses HTTP connection):
        >>> async with AsyncAmazonCreatorsApi(
        ...     credential_id="your_id",
        ...     credential_secret="your_secret",
        ...     version="2.2",
        ...     tag="your-tag",
        ...     country="ES"
        ... ) as api:
        ...     items = await api.get_items(["B0DLFMFBJW"])

    The context manager approach is more efficient when making multiple
    requests in quick succession due to HTTP connection pooling.

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
        """Initialize the async Amazon Creators API client."""
        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self._last_query_time = time.time() - throttling
        self.tag = tag
        self.throttling = float(throttling)

        # Determine marketplace from country or direct value
        if marketplace:
            self.marketplace = marketplace
        elif country:
            if country not in MARKETPLACES:
                msg = f"Country code '{country}' is not valid"
                raise InvalidArgumentError(msg)
            self.marketplace = MARKETPLACES[country]
        else:
            msg = "Either 'country' or 'marketplace' must be provided"
            raise InvalidArgumentError(msg)

        # HTTP client and token manager (initialized lazily or via context manager)
        self._http_client: AsyncHttpClient | None = None
        self._token_manager = AsyncOAuth2TokenManager(
            credential_id=credential_id,
            credential_secret=credential_secret,
            version=version,
        )
        self._owns_client = False

    async def __aenter__(self) -> Self:
        """Enter async context manager, creating a persistent HTTP client."""
        self._http_client = AsyncHttpClient(host=API_HOST)
        await self._http_client.__aenter__()
        self._owns_client = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager, closing the HTTP client."""
        if self._http_client is not None and self._owns_client:
            await self._http_client.__aexit__(exc_type, exc_val, exc_tb)
            self._http_client = None
            self._owns_client = False

    async def get_items(
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
            resources = self._get_all_resources(GetItemsResource)

        item_ids = get_items_ids(items)

        request_body = {
            "partnerTag": self.tag,
            "itemIds": item_ids,
            "resources": [r.value for r in resources],
        }
        if condition is not None:
            request_body["condition"] = condition.value
        if currency_of_preference is not None:
            request_body["currencyOfPreference"] = currency_of_preference
        if languages_of_preference is not None:
            request_body["languagesOfPreference"] = languages_of_preference

        response = await self._make_request(ENDPOINT_GET_ITEMS, request_body)

        items_result = response.get("itemsResult")
        if items_result is None or items_result.get("items") is None:
            msg = "No items have been found"
            raise ItemsNotFoundError(msg)

        return self._deserialize_items(items_result["items"])

    async def search_items(  # noqa: PLR0912, C901
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
            resources = self._get_all_resources(SearchItemsResource)

        request_body: dict[str, Any] = {
            "partnerTag": self.tag,
            "resources": [r.value for r in resources],
        }

        # Add optional parameters
        if keywords is not None:
            request_body["keywords"] = keywords
        if actor is not None:
            request_body["actor"] = actor
        if artist is not None:
            request_body["artist"] = artist
        if author is not None:
            request_body["author"] = author
        if brand is not None:
            request_body["brand"] = brand
        if title is not None:
            request_body["title"] = title
        if browse_node_id is not None:
            request_body["browseNodeId"] = browse_node_id
        if search_index is not None:
            request_body["searchIndex"] = search_index
        if item_count is not None:
            request_body["itemCount"] = item_count
        if item_page is not None:
            request_body["itemPage"] = item_page
        if condition is not None:
            request_body["condition"] = condition.value
        if currency_of_preference is not None:
            request_body["currencyOfPreference"] = currency_of_preference
        if languages_of_preference is not None:
            request_body["languagesOfPreference"] = languages_of_preference
        if max_price is not None:
            request_body["maxPrice"] = max_price
        if min_price is not None:
            request_body["minPrice"] = min_price
        if min_saving_percent is not None:
            request_body["minSavingPercent"] = min_saving_percent
        if min_reviews_rating is not None:
            request_body["minReviewsRating"] = min_reviews_rating
        if sort_by is not None:
            request_body["sortBy"] = sort_by.value

        response = await self._make_request(ENDPOINT_SEARCH_ITEMS, request_body)

        search_result = response.get("searchResult")
        if search_result is None:
            msg = "No items have been found"
            raise ItemsNotFoundError(msg)

        return self._deserialize_search_result(search_result)

    async def get_variations(
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
            resources = self._get_all_resources(GetVariationsResource)

        asin = get_asin(asin)

        request_body: dict[str, Any] = {
            "partnerTag": self.tag,
            "asin": asin,
            "resources": [r.value for r in resources],
        }

        if variation_count is not None:
            request_body["variationCount"] = variation_count
        if variation_page is not None:
            request_body["variationPage"] = variation_page
        if condition is not None:
            request_body["condition"] = condition.value
        if currency_of_preference is not None:
            request_body["currencyOfPreference"] = currency_of_preference
        if languages_of_preference is not None:
            request_body["languagesOfPreference"] = languages_of_preference

        response = await self._make_request(ENDPOINT_GET_VARIATIONS, request_body)

        variations_result = response.get("variationsResult")
        if variations_result is None:
            msg = "No variations have been found"
            raise ItemsNotFoundError(msg)

        return self._deserialize_variations_result(variations_result)

    async def get_browse_nodes(
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
            resources = self._get_all_resources(GetBrowseNodesResource)

        request_body: dict[str, Any] = {
            "partnerTag": self.tag,
            "browseNodeIds": browse_node_ids,
            "resources": [r.value for r in resources],
        }

        if languages_of_preference is not None:
            request_body["languagesOfPreference"] = languages_of_preference

        response = await self._make_request(ENDPOINT_GET_BROWSE_NODES, request_body)

        browse_nodes_result = response.get("browseNodesResult")
        if (
            browse_nodes_result is None
            or browse_nodes_result.get("browseNodes") is None
        ):
            msg = "No browse nodes have been found"
            raise ItemsNotFoundError(msg)

        return self._deserialize_browse_nodes(browse_nodes_result["browseNodes"])

    async def _throttle(self) -> None:
        """Wait for the throttling interval to elapse since the last API call."""
        wait_time = self.throttling - (time.time() - self._last_query_time)
        if wait_time > 0:
            await asyncio.sleep(wait_time)
        self._last_query_time = time.time()

    async def _make_request(
        self,
        endpoint: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """Make an API request with authentication and throttling.

        Args:
            endpoint: API endpoint path.
            body: Request body.

        Returns:
            Parsed JSON response.

        Raises:
            Various exceptions based on API errors.

        """
        await self._throttle()

        # Get auth token
        token = await self._token_manager.get_token()

        headers = {
            "Authorization": f"Bearer {token}, Version {self._version}",
            "Content-Type": "application/json; charset=utf-8",
            "x-marketplace": self.marketplace,
        }

        # Use persistent client if available, otherwise create a new one
        if self._http_client is not None:
            response = await self._http_client.post(endpoint, headers, body)
        else:
            async with AsyncHttpClient(host=API_HOST) as client:
                response = await client.post(endpoint, headers, body)

        # Handle errors
        if response.status_code != 200:  # noqa: PLR2004
            self._handle_error_response(response.status_code, response.text)

        return response.json()

    def _handle_error_response(self, status_code: int, body: str) -> None:
        """Handle API error responses and raise appropriate exceptions.

        Args:
            status_code: HTTP status code.
            body: Response body text.

        Raises:
            ItemsNotFoundError: For 404 errors.
            TooManyRequestsError: For 429 errors.
            InvalidArgumentError: For validation errors.
            AssociateValidationError: For invalid associate credentials.
            RequestError: For other errors.

        """
        http_not_found = 404
        http_too_many_requests = 429

        if status_code == http_not_found:
            msg = "No items found for the request"
            raise ItemsNotFoundError(msg)

        if status_code == http_too_many_requests:
            msg = "Rate limit exceeded, try increasing throttling"
            raise TooManyRequestsError(msg)

        if "InvalidParameterValue" in body:
            msg = "Invalid parameter value provided in the request"
            raise InvalidArgumentError(msg)

        if "InvalidPartnerTag" in body:
            msg = "The partner tag is invalid or not present"
            raise InvalidArgumentError(msg)

        if "InvalidAssociate" in body:
            msg = "Credentials are not valid for the selected marketplace"
            raise AssociateValidationError(msg)

        # Generic error
        body_info = f" - {body[:200]}" if body else ""
        msg = f"Request failed with status {status_code}{body_info}"
        raise RequestError(msg)

    def _get_all_resources(self, resource_class: type[Enum]) -> list[Any]:
        """Extract all resource values from a resource enum class."""
        return list(resource_class)

    def _deserialize_items(self, items_data: list[dict[str, Any]]) -> list[Item]:
        """Deserialize item data from API response to Item models."""
        return [Item.model_validate(item) for item in items_data]

    def _deserialize_search_result(
        self,
        search_result_data: dict[str, Any],
    ) -> SearchResult:
        """Deserialize search result data from API response to SearchResult model."""
        return SearchResult.model_validate(search_result_data)

    def _deserialize_variations_result(
        self,
        variations_result_data: dict[str, Any],
    ) -> VariationsResult:
        """Deserialize variations data from API response to VariationsResult model."""
        return VariationsResult.model_validate(variations_result_data)

    def _deserialize_browse_nodes(
        self,
        browse_nodes_data: list[dict[str, Any]],
    ) -> list[BrowseNode]:
        """Deserialize browse nodes data from API response to BrowseNode models."""
        return [BrowseNode.model_validate(node) for node in browse_nodes_data]
