"""Async Amazon Creators API wrapper for Python.

Provides async methods to interact with the Amazon Creators API.
"""

from __future__ import annotations

import asyncio
import time
from enum import Enum
from typing import TYPE_CHECKING, Any, TypeVar

from typing_extensions import Self

from amazon_creatorsapi.core.constants import (
    DEFAULT_HOST,
    DEFAULT_THROTTLING,
    DEFAULT_TIMEOUT,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
)
from amazon_creatorsapi.core.error_handling import format_errors, handle_api_error
from amazon_creatorsapi.core.items import (
    get_item_chunks,
    get_unique_items,
    sort_items,
)
from amazon_creatorsapi.core.oauth import build_authorization_header, get_auth_endpoint
from amazon_creatorsapi.core.parsers import get_asin, get_items_ids
from amazon_creatorsapi.core.requests import get_request_body
from amazon_creatorsapi.core.resources import get_all_resources
from amazon_creatorsapi.core.results import ResultList
from amazon_creatorsapi.core.retry import DEFAULT_RETRIES, get_retry_delay, is_retryable
from amazon_creatorsapi.core.validation import (
    build_request,
    validate_and_get_marketplace,
    validate_retries,
    validate_search_criteria,
    validate_throttling,
    validate_timeout,
)
from amazon_creatorsapi.errors import (
    AmazonCreatorsApiError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
)

try:
    import httpx

    from .auth import AsyncOAuth2TokenManager
    from .client import AsyncHttpClient, AsyncHttpResponse
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc

from creatorsapi_python_sdk.models.get_browse_nodes_request_content import (
    GetBrowseNodesRequestContent,
)
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_feed_request_content import (
    GetFeedRequestContent,
)
from creatorsapi_python_sdk.models.get_items_request_content import (
    GetItemsRequestContent,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_report_request_content import (
    GetReportRequestContent,
)
from creatorsapi_python_sdk.models.get_variations_request_content import (
    GetVariationsRequestContent,
)
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.search_items_request_content import (
    SearchItemsRequestContent,
)
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource

if TYPE_CHECKING:
    from types import TracebackType

    from amazon_creatorsapi.core.marketplaces import CountryCode
    from creatorsapi_python_sdk.models.availability import Availability
    from creatorsapi_python_sdk.models.condition import Condition
    from creatorsapi_python_sdk.models.delivery_flag import DeliveryFlag
    from creatorsapi_python_sdk.models.feed_type import FeedType
    from creatorsapi_python_sdk.models.report_type import ReportType
    from creatorsapi_python_sdk.models.sort_by import SortBy

from creatorsapi_python_sdk.models.browse_node import BrowseNode
from creatorsapi_python_sdk.models.error_data import ErrorData
from creatorsapi_python_sdk.models.feed import Feed
from creatorsapi_python_sdk.models.get_feed_response_content import (
    GetFeedResponseContent,
)
from creatorsapi_python_sdk.models.get_report_response_content import (
    GetReportResponseContent,
)
from creatorsapi_python_sdk.models.item import Item
from creatorsapi_python_sdk.models.report_metadata import ReportMetadata
from creatorsapi_python_sdk.models.search_result import SearchResult
from creatorsapi_python_sdk.models.variations_result import VariationsResult

# API endpoints
API_HOST = DEFAULT_HOST
ENDPOINT_GET_ITEMS = "/catalog/v1/getItems"
ENDPOINT_SEARCH_ITEMS = "/catalog/v1/searchItems"
ENDPOINT_GET_VARIATIONS = "/catalog/v1/getVariations"
ENDPOINT_GET_BROWSE_NODES = "/catalog/v1/getBrowseNodes"
ENDPOINT_LIST_FEEDS = "/catalog/v1/listFeeds"
ENDPOINT_GET_FEED = "/catalog/v1/getFeed"
ENDPOINT_LIST_REPORTS = "/reports/v1/listReports"
ENDPOINT_GET_REPORT = "/reports/v1/getReport"

# TypeVar for generic resource handling
ResourceT = TypeVar("ResourceT", bound=Enum)


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

    Note:
        Using without context manager creates a new HTTP connection for each
        request, which is less efficient and may impact performance. For
        production code making multiple API calls, always use the context
        manager (async with) to benefit from connection pooling and reduced
        overhead.

    Args:
        credential_id: Your Creators API credential ID.
        credential_secret: Your Creators API credential secret.
        version: API version for your region.
        tag: Your affiliate tracking id (partner tag).
        country: Country code (e.g., "ES", "US"). Used to determine marketplace.
        marketplace: Marketplace URL (e.g., "www.amazon.es"). Overrides country.
        throttling: Wait time in seconds between API calls. Defaults to 1 second.
        timeout: Request timeout in seconds, or None to wait indefinitely.
            Defaults to 30 seconds.
        retries: Extra attempts for the failures that Amazon asks to retry,
            waiting longer before every attempt. Defaults to 3.
        host: Base URL of the API. Defaults to the Amazon Creators API.
        auth_endpoint: URL used to get the OAuth2 token. Defaults to the one
            of the version in use.

    Raises:
        InvalidArgumentError: If neither country nor marketplace is provided,
            if timeout is not greater than zero, if throttling is negative,
            if retries is negative, if the version is not one of the supported
            ones, which the message of the error lists, and no auth_endpoint
            is given, or if it belongs to a family that the library cannot
            authenticate (2.x and 3.x are the supported ones), which no
            auth_endpoint makes valid.

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
        timeout: float | None = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        host: str = DEFAULT_HOST,
        auth_endpoint: str | None = None,
    ) -> None:
        """Initialize the async Amazon Creators API client."""
        # Resolve the endpoint early to fail fast on an unsupported version,
        # which a custom endpoint makes valid
        endpoint = get_auth_endpoint(version, auth_endpoint)

        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self.host = host
        self._throttle_lock: asyncio.Lock | None = None
        self.tag = tag
        self.throttling = validate_throttling(throttling)
        self.timeout = validate_timeout(timeout)
        self.retries = validate_retries(retries)
        self._last_query_time = time.monotonic() - self.throttling

        # Determine marketplace from country or direct value
        self.marketplace = validate_and_get_marketplace(country, marketplace)

        # HTTP client and token manager (initialized lazily or via context manager)
        self._http_client: AsyncHttpClient | None = None
        self._token_manager = AsyncOAuth2TokenManager(
            credential_id=credential_id,
            credential_secret=credential_secret,
            version=version,
            auth_endpoint=endpoint,
            timeout=self.timeout,
        )
        self._owns_client = False

    async def __aenter__(self) -> Self:
        """Enter async context manager, creating a persistent HTTP client."""
        self._http_client = AsyncHttpClient(host=self.host, timeout=self.timeout)
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
        *,
        include_unavailable: bool = False,
    ) -> ResultList[Item]:
        """Get items information from Amazon.

        Duplicated items are requested only once, and the request is split into
        as many API calls as needed when it goes over the limit of items that
        Amazon accepts at once. A call that keeps failing after the retries
        raises, discarding the items returned by the previous calls.

        Args:
            items: One or more items, using ASIN or Amazon product URL.
                Accepts a single string (comma-separated) or a list of strings.
            condition: Filter offers by condition type.
            currency_of_preference: ISO 4217 currency code for prices.
            languages_of_preference: Languages in order of preference.
            resources: List of resources to retrieve. Defaults to all.
            include_unavailable: Add an item holding only the ASIN for every
                requested item missing from the response. Defaults to False.

        Returns:
            List of Item objects with Amazon information, in the order of the
            requested items, exposing the partial errors of the response in
            its errors attribute.

        Raises:
            ItemsNotFoundError: If no items are found.
            InvalidArgumentError: If parameters are invalid.

        """
        if resources is None:
            resources = get_all_resources(GetItemsResource)

        item_ids = get_unique_items(get_items_ids(items))

        if not item_ids:
            msg = "At least one item is required"
            raise InvalidArgumentError(msg)

        found_items: list[Item] = []
        errors: list[ErrorData] = []

        for chunk in get_item_chunks(item_ids):
            request = build_request(
                GetItemsRequestContent,
                partnerTag=self.tag,
                itemIds=chunk,
                condition=condition,
                currencyOfPreference=currency_of_preference,
                languagesOfPreference=languages_of_preference,
                resources=resources,
            )

            response = await self._make_request(
                ENDPOINT_GET_ITEMS,
                get_request_body(request),
            )

            errors.extend(self._deserialize_errors(response))

            items_result = response.get("itemsResult") or {}
            if items_result.get("items"):
                found_items.extend(self._deserialize_items(items_result["items"]))

        sorted_items = sort_items(
            found_items,
            item_ids,
            include_unavailable=include_unavailable,
        )

        if not sorted_items and not include_unavailable:
            msg = f"No items have been found{format_errors(errors)}"
            raise ItemsNotFoundError(msg)

        return ResultList(sorted_items, errors=errors)

    async def search_items(
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
        delivery_flags: list[DeliveryFlag] | None = None,
        languages_of_preference: list[str] | None = None,
        max_price: int | None = None,
        min_price: int | None = None,
        min_saving_percent: int | None = None,
        min_reviews_rating: int | None = None,
        sort_by: SortBy | None = None,
        resources: list[SearchItemsResource] | None = None,
        *,
        availability: Availability | None = None,
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
            item_count: Number of items returned (1-100). Defaults to 10.
            item_page: Page of items to return (1-10). Defaults to 1.
            condition: Filter offers by condition type.
            currency_of_preference: ISO 4217 currency code for prices.
            delivery_flags: Delivery programs to filter search results by.
            languages_of_preference: Languages in order of preference.
            max_price: Max price in lowest currency denomination.
            min_price: Min price in lowest currency denomination.
            min_saving_percent: Min savings percentage (1-99).
            min_reviews_rating: Min review rating (1-4).
            sort_by: Sort method for results.
            resources: List of resources to retrieve. Defaults to all.
            availability: Filter results by availability. Defaults to
                returning only the items available for purchase. Keyword only,
                so it does not shift the position of the other arguments.

        Returns:
            SearchResult containing the list of items.

        Raises:
            ItemsNotFoundError: If no items are found.

        """
        validate_search_criteria(
            keywords=keywords,
            actor=actor,
            artist=artist,
            author=author,
            brand=brand,
            title=title,
            browse_node_id=browse_node_id,
            search_index=search_index,
        )

        if resources is None:
            resources = get_all_resources(SearchItemsResource)

        request = build_request(
            SearchItemsRequestContent,
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
            availability=availability,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            deliveryFlags=delivery_flags,
            languagesOfPreference=languages_of_preference,
            maxPrice=max_price,
            minPrice=min_price,
            minSavingPercent=min_saving_percent,
            minReviewsRating=min_reviews_rating,
            sortBy=sort_by,
            resources=resources,
        )

        response = await self._make_request(
            ENDPOINT_SEARCH_ITEMS,
            get_request_body(request),
        )

        search_result = response.get("searchResult")
        if search_result is None:
            errors = self._deserialize_errors(response)
            msg = f"No items have been found{format_errors(errors)}"
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
            variation_page: Page of variations to return (1 or above).
                Defaults to 1.
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

        request = build_request(
            GetVariationsRequestContent,
            partnerTag=self.tag,
            asin=get_asin(asin),
            variationCount=variation_count,
            variationPage=variation_page,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        response = await self._make_request(
            ENDPOINT_GET_VARIATIONS,
            get_request_body(request),
        )

        variations_result = response.get("variationsResult")
        if variations_result is None:
            errors = self._deserialize_errors(response)
            msg = f"No variations have been found{format_errors(errors)}"
            raise ItemsNotFoundError(msg)

        return self._deserialize_variations_result(variations_result)

    async def get_browse_nodes(
        self,
        browse_node_ids: list[str],
        languages_of_preference: list[str] | None = None,
        resources: list[GetBrowseNodesResource] | None = None,
    ) -> ResultList[BrowseNode]:
        """Return browse node information including name, children, and ancestors.

        Args:
            browse_node_ids: List of browse node IDs.
            languages_of_preference: Languages in order of preference.
            resources: List of resources to retrieve. Defaults to all.

        Returns:
            List of BrowseNode objects, exposing the partial errors of the
            response in its errors attribute.

        Raises:
            ItemsNotFoundError: If no browse nodes are found.

        """
        if resources is None:
            resources = get_all_resources(GetBrowseNodesResource)

        request = build_request(
            GetBrowseNodesRequestContent,
            partnerTag=self.tag,
            browseNodeIds=browse_node_ids,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        response = await self._make_request(
            ENDPOINT_GET_BROWSE_NODES,
            get_request_body(request),
        )

        errors = self._deserialize_errors(response)
        browse_nodes_result = response.get("browseNodesResult")
        if (
            browse_nodes_result is None
            or browse_nodes_result.get("browseNodes") is None
        ):
            msg = f"No browse nodes have been found{format_errors(errors)}"
            raise ItemsNotFoundError(msg)

        return ResultList(
            self._deserialize_browse_nodes(browse_nodes_result["browseNodes"]),
            errors=errors,
        )

    async def list_feeds(self) -> list[Feed]:
        """Return the feeds available for your account.

        Returns:
            List of Feed objects, empty if no feeds are available. Each feed
            carries its type, so the same name can exist in more than one
            feed program.

        Raises:
            RequestError: If the API request fails.

        """
        response = await self._make_request(
            ENDPOINT_LIST_FEEDS,
            not_found_error=ResourceNotFoundError,
        )

        return self._deserialize_feeds(response.get("feeds") or [])

    async def get_feed(self, feed_name: str, feed_type: FeedType | None = None) -> str:
        """Return a temporary download URL for a feed.

        Args:
            feed_name: Name of the feed, as returned by list_feeds.
            feed_type: Feed program the name belongs to. Needed to disambiguate
                a name available in more than one program.

        Returns:
            URL to download the feed contents from.

        Raises:
            RequestError: If the API request fails.

        """
        request = build_request(
            GetFeedRequestContent,
            feedName=feed_name,
            feedType=feed_type,
        )

        response = await self._make_request(
            ENDPOINT_GET_FEED,
            get_request_body(request),
            not_found_error=ResourceNotFoundError,
        )

        return GetFeedResponseContent.model_validate(response).url

    async def list_reports(self) -> list[ReportMetadata]:
        """Return the reports available for your account.

        Returns:
            List of ReportMetadata objects, empty if no reports are available.
            Each report carries its type, telling Creator Central reports apart
            from Creator Connections ones.

        Raises:
            RequestError: If the API request fails.

        """
        response = await self._make_request(
            ENDPOINT_LIST_REPORTS,
            not_found_error=ResourceNotFoundError,
        )

        return self._deserialize_reports(response.get("reports") or [])

    async def get_report(
        self,
        filename: str,
        report_type: ReportType | None = None,
    ) -> str:
        """Return a temporary download URL for a report.

        Args:
            filename: Name of the report, as returned by list_reports.
            report_type: Program the report belongs to. Needed to disambiguate
                a filename available in more than one program.

        Returns:
            URL to download the report contents from.

        Raises:
            RequestError: If the API request fails.

        """
        request = build_request(
            GetReportRequestContent,
            filename=filename,
            reportType=report_type,
        )

        response = await self._make_request(
            ENDPOINT_GET_REPORT,
            get_request_body(request),
            not_found_error=ResourceNotFoundError,
        )

        return GetReportResponseContent.model_validate(response).url

    async def _throttle(self) -> None:
        """Wait for the throttling interval to elapse since the last API call.

        Uses asyncio.Lock to prevent race conditions when multiple coroutines
        attempt to make concurrent requests.
        """
        # Lazy initialization of the lock (ensures event loop is active)
        if self._throttle_lock is None:
            self._throttle_lock = asyncio.Lock()

        async with self._throttle_lock:
            wait_time = self.throttling - (time.monotonic() - self._last_query_time)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self._last_query_time = time.monotonic()

    async def _make_request(
        self,
        endpoint: str,
        body: dict[str, Any] | None = None,
        not_found_error: type[AmazonCreatorsApiError] = ItemsNotFoundError,
    ) -> dict[str, Any]:
        """Make an API request with authentication, throttling and retries.

        Throttled and server errors are retried waiting longer before every
        attempt, honouring the Retry-After header when the API sends it. An
        expired token is refreshed once and the request is sent again.

        Args:
            endpoint: API endpoint path.
            body: Request body, omitted for operations that take no payload.
            not_found_error: Exception raised when the resource is missing.

        Returns:
            Parsed JSON response.

        Raises:
            RequestError: If the request cannot be completed.

        """
        attempt = 0
        token_refreshed = False

        while True:
            await self._throttle()

            try:
                response = await self._post(endpoint, body)
            except httpx.HTTPError as error:
                if attempt >= self.retries:
                    msg = f"Request failed: {error}"
                    raise RequestError(msg) from error
                await asyncio.sleep(get_retry_delay(attempt))
                attempt += 1
                continue

            if response.status_code == HTTP_OK:
                return self._parse_response(response)

            if response.status_code == HTTP_UNAUTHORIZED and not token_refreshed:
                token_refreshed = True
                self._token_manager.clear_token()
                continue

            if not is_retryable(response.status_code) or attempt >= self.retries:
                handle_api_error(
                    response.status_code,
                    response.text,
                    not_found_error,
                    response.headers,
                )

            await asyncio.sleep(get_retry_delay(attempt, response.headers))
            attempt += 1

    async def _post(
        self,
        endpoint: str,
        body: dict[str, Any] | None,
    ) -> AsyncHttpResponse:
        """Send an authenticated request to the API.

        Args:
            endpoint: API endpoint path.
            body: Request body, omitted for operations that take no payload.

        Returns:
            The response of the API.

        """
        token = await self._token_manager.get_token()

        headers = {
            "Authorization": self._build_authorization_header(token),
            "Content-Type": "application/json; charset=utf-8",
            "x-marketplace": self.marketplace,
        }

        # Use persistent client if available, otherwise create a new one
        if self._http_client is not None:
            return await self._http_client.post(endpoint, headers, body)

        async with AsyncHttpClient(host=self.host, timeout=self.timeout) as client:
            return await client.post(endpoint, headers, body)

    def _parse_response(self, response: AsyncHttpResponse) -> dict[str, Any]:
        """Parse a successful response as JSON.

        Args:
            response: Response of the API.

        Returns:
            The parsed response body.

        Raises:
            RequestError: If the response is not valid JSON.

        """
        try:
            return response.json()
        except ValueError as error:
            msg = f"Failed to parse the response from Amazon: {error}"
            raise RequestError(msg) from error

    def _build_authorization_header(self, token: str) -> str:
        """Build the version-appropriate Authorization header."""
        return build_authorization_header(self._version, token)

    def _deserialize_errors(self, response: dict[str, Any]) -> list[ErrorData]:
        """Deserialize the partial errors of a response to ErrorData models."""
        return [
            ErrorData.model_validate(error) for error in response.get("errors") or []
        ]

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

    def _deserialize_feeds(self, feeds_data: list[dict[str, Any]]) -> list[Feed]:
        """Deserialize feed data from API response to Feed models."""
        return [Feed.model_validate(feed) for feed in feeds_data]

    def _deserialize_reports(
        self,
        reports_data: list[dict[str, Any]],
    ) -> list[ReportMetadata]:
        """Deserialize report data from API response to ReportMetadata models."""
        return [ReportMetadata.model_validate(report) for report in reports_data]
