"""Amazon Creators API wrapper for Python.

A Python wrapper for the Amazon Creators API.
"""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, Any, Callable, NoReturn, TypeVar

import urllib3

from amazon_creatorsapi.core.auth import TimeoutOAuth2TokenManager
from amazon_creatorsapi.core.constants import (
    DEFAULT_HOST,
    DEFAULT_THROTTLING,
    DEFAULT_TIMEOUT,
    HTTP_UNAUTHORIZED,
)
from amazon_creatorsapi.core.error_handling import format_errors, handle_api_error
from amazon_creatorsapi.core.items import (
    get_item_chunks,
    get_unique_items,
    sort_items,
)
from amazon_creatorsapi.core.oauth import get_auth_endpoint
from amazon_creatorsapi.core.parsers import get_asin, get_items_ids
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
from creatorsapi_python_sdk.api.default_api import DefaultApi
from creatorsapi_python_sdk.api_client import ApiClient
from creatorsapi_python_sdk.auth.oauth2_config import OAuth2Config
from creatorsapi_python_sdk.configuration import Configuration
from creatorsapi_python_sdk.exceptions import ApiException
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
    from creatorsapi_python_sdk.models.browse_node import BrowseNode
    from creatorsapi_python_sdk.models.condition import Condition
    from creatorsapi_python_sdk.models.delivery_flag import DeliveryFlag
    from creatorsapi_python_sdk.models.error_data import ErrorData
    from creatorsapi_python_sdk.models.feed import Feed
    from creatorsapi_python_sdk.models.feed_type import FeedType
    from creatorsapi_python_sdk.models.item import Item
    from creatorsapi_python_sdk.models.report_metadata import ReportMetadata
    from creatorsapi_python_sdk.models.report_type import ReportType
    from creatorsapi_python_sdk.models.search_result import SearchResult
    from creatorsapi_python_sdk.models.sort_by import SortBy
    from creatorsapi_python_sdk.models.variations_result import VariationsResult

ResponseT = TypeVar("ResponseT")
# typing.Self needs Python 3.11 and typing_extensions is only required by the
# async extra, so the client is typed with a TypeVar bound to itself
ClientT = TypeVar("ClientT", bound="AmazonCreatorsApi")


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

    Example:
        >>> api = AmazonCreatorsApi(
        ...     credential_id="your_id",
        ...     credential_secret="your_secret",
        ...     version="2.2",
        ...     tag="your-tag",
        ...     country="ES"
        ... )
        >>> items = api.get_items(["B0DLFMFBJW"])

    The client keeps a pool of connections open, so it is meant to be reused.
    Call close, or use it as a context manager, to release the connections of
    a client that is not going to be used again.

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
        """Initialize the Amazon Creators API client."""
        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self._throttle_lock = threading.Lock()
        self.tag = tag
        self.throttling = validate_throttling(throttling)
        self.timeout = validate_timeout(timeout)
        self.retries = validate_retries(retries)
        self._last_query_time = time.monotonic() - self.throttling

        # Determine marketplace from country or direct value
        self.marketplace = validate_and_get_marketplace(country, marketplace)

        # The endpoint is resolved here, so both clients share the same list
        # of versions instead of relying on the one bundled with the SDK
        endpoint = get_auth_endpoint(version, auth_endpoint)

        # A new configuration for every client, as the default one of the
        # SDK is shared by the whole process
        self._api_client = ApiClient(
            configuration=Configuration(),
            credential_id=credential_id,
            credential_secret=credential_secret,
            version=version,
            host=host,
            auth_endpoint=endpoint,
        )
        # The token manager bundled with the SDK requests the token without
        # any timeout, so it is replaced by one that honours the configured
        # value and reports failures as library errors.
        self._api_client._token_manager = TimeoutOAuth2TokenManager(  # noqa: SLF001
            OAuth2Config(credential_id, credential_secret, version, endpoint),
            self.timeout,
        )
        self._api = DefaultApi(self._api_client)

    def __enter__(self: ClientT) -> ClientT:  # noqa: PYI019
        """Return the client, which closes its connections when leaving."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Close the connections of the client."""
        self.close()

    def close(self) -> None:
        """Release the connections kept open by the client.

        The client stays usable after closing it, opening a new connection on
        the next request. Calling it is only needed for clients that are not
        reused, as the ones created for a single request.
        """
        self._api_client.rest_client.pool_manager.clear()

    def get_items(
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

            response = self._call(
                self._api.get_items,
                get_items_request_content=request,
            )

            errors.extend(response.errors or [])

            if response.items_result is not None and response.items_result.items:
                found_items.extend(response.items_result.items)

        sorted_items = sort_items(
            found_items,
            item_ids,
            include_unavailable=include_unavailable,
        )

        if not sorted_items and not include_unavailable:
            msg = f"No items have been found{format_errors(errors)}"
            raise ItemsNotFoundError(msg)

        return ResultList(sorted_items, errors=errors)

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

        response = self._call(
            self._api.search_items,
            search_items_request_content=request,
        )

        if response.search_result is None:
            msg = f"No items have been found{format_errors(response.errors)}"
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

        asin = get_asin(asin)

        request = build_request(
            GetVariationsRequestContent,
            partnerTag=self.tag,
            asin=asin,
            variationCount=variation_count,
            variationPage=variation_page,
            condition=condition,
            currencyOfPreference=currency_of_preference,
            languagesOfPreference=languages_of_preference,
            resources=resources,
        )

        response = self._call(
            self._api.get_variations,
            get_variations_request_content=request,
        )

        if response.variations_result is None:
            msg = f"No variations have been found{format_errors(response.errors)}"
            raise ItemsNotFoundError(msg)

        return response.variations_result

    def get_browse_nodes(
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

        response = self._call(
            self._api.get_browse_nodes,
            get_browse_nodes_request_content=request,
        )

        if (
            response.browse_nodes_result is None
            or response.browse_nodes_result.browse_nodes is None
        ):
            msg = f"No browse nodes have been found{format_errors(response.errors)}"
            raise ItemsNotFoundError(msg)

        return ResultList(
            response.browse_nodes_result.browse_nodes,
            errors=response.errors,
        )

    def list_feeds(self) -> list[Feed]:
        """Return the feeds available for your account.

        Returns:
            List of Feed objects, empty if no feeds are available. Each feed
            carries its type, so the same name can exist in more than one
            feed program.

        Raises:
            RequestError: If the API request fails.

        """
        response = self._call(
            self._api.list_feeds,
            not_found_error=ResourceNotFoundError,
        )

        return response.feeds or []

    def get_feed(self, feed_name: str, feed_type: FeedType | None = None) -> str:
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

        response = self._call(
            self._api.get_feed,
            not_found_error=ResourceNotFoundError,
            get_feed_request_content=request,
        )

        return response.url

    def list_reports(self) -> list[ReportMetadata]:
        """Return the reports available for your account.

        Returns:
            List of ReportMetadata objects, empty if no reports are available.
            Each report carries its type, telling Creator Central reports apart
            from Creator Connections ones.

        Raises:
            RequestError: If the API request fails.

        """
        response = self._call(
            self._api.list_reports,
            not_found_error=ResourceNotFoundError,
        )

        return response.reports

    def get_report(self, filename: str, report_type: ReportType | None = None) -> str:
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

        response = self._call(
            self._api.get_report,
            not_found_error=ResourceNotFoundError,
            get_report_request_content=request,
        )

        return response.url

    def _throttle(self) -> None:
        """Wait for the throttling interval to elapse since the last API call.

        Uses a lock to keep the interval between calls when the client is
        shared by several threads.
        """
        with self._throttle_lock:
            wait_time = self.throttling - (time.monotonic() - self._last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self._last_query_time = time.monotonic()

    def _call(
        self,
        operation: Callable[..., ResponseT],
        *,
        not_found_error: type[AmazonCreatorsApiError] = ItemsNotFoundError,
        **kwargs: Any,
    ) -> ResponseT:
        """Call an operation of the SDK, retrying the failures worth retrying.

        Throttled and server errors are retried waiting longer before every
        attempt, honouring the Retry-After header when the API sends it. An
        expired token is refreshed once and the request is sent again.

        Args:
            operation: Operation of the SDK to call.
            not_found_error: Exception raised when the resource is missing.
            kwargs: Arguments for the operation.

        Returns:
            The response of the operation.

        Raises:
            RequestError: If the request cannot be completed.

        """
        attempt = 0
        token_refreshed = False

        while True:
            self._throttle()

            try:
                return operation(
                    x_marketplace=self.marketplace,
                    _request_timeout=self.timeout,
                    **kwargs,
                )
            except ApiException as error:
                if error.status == HTTP_UNAUTHORIZED and not token_refreshed:
                    token_refreshed = True
                    self._clear_token()
                    continue

                if not is_retryable(error.status) or attempt >= self.retries:
                    self._handle_api_exception(error, not_found_error)

                time.sleep(get_retry_delay(attempt, error.headers))
            except urllib3.exceptions.HTTPError as error:
                if attempt >= self.retries:
                    msg = f"Request failed: {error}"
                    raise RequestError(msg) from error

                time.sleep(get_retry_delay(attempt))

            attempt += 1

    def _clear_token(self) -> None:
        """Discard the cached token so the next request asks for a new one."""
        token_manager = self._api_client.token_manager
        if token_manager is not None:
            token_manager.clear_token()

    def _handle_api_exception(
        self,
        error: ApiException,
        not_found_error: type[AmazonCreatorsApiError] = ItemsNotFoundError,
    ) -> NoReturn:
        """Handle API exceptions and raise appropriate custom exceptions."""
        body = error.body if isinstance(error.body, str) else ""
        reason = str(error.reason) if error.reason else None

        try:
            handle_api_error(
                error.status,
                body,
                not_found_error,
                error.headers,
                reason,
            )
        except AmazonCreatorsApiError as exc:
            # Re-raise with original exception as cause for better stack traces
            raise exc from error
