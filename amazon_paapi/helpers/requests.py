"""Module with helper functions for creating requests."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, List, NoReturn, cast

from amazon_paapi.errors import (
    AssociateValidationError,
    InvalidArgument,
    ItemsNotFound,
    MalformedRequest,
    RequestError,
    TooManyRequests,
)
from amazon_paapi.models.browse_nodes_result import BrowseNode
from amazon_paapi.models.item_result import Item
from amazon_paapi.models.search_result import SearchResult
from amazon_paapi.models.variations_result import VariationsResult
from amazon_paapi.sdk.models.get_browse_nodes_request import GetBrowseNodesRequest
from amazon_paapi.sdk.models.get_browse_nodes_resource import GetBrowseNodesResource
from amazon_paapi.sdk.models.get_items_request import GetItemsRequest
from amazon_paapi.sdk.models.get_items_resource import GetItemsResource
from amazon_paapi.sdk.models.get_variations_request import GetVariationsRequest
from amazon_paapi.sdk.models.get_variations_resource import GetVariationsResource
from amazon_paapi.sdk.models.partner_type import PartnerType
from amazon_paapi.sdk.models.search_items_request import SearchItemsRequest
from amazon_paapi.sdk.models.search_items_resource import SearchItemsResource
from amazon_paapi.sdk.rest import ApiException
from amazon_paapi.sdk.rest import ApiException as ApiExceptionType

if TYPE_CHECKING:
    from amazon_paapi.api import AmazonApi


def get_items_request(
    amazon_api: AmazonApi,
    asin_chunk: list[str],
    **kwargs: Any,
) -> GetItemsRequest:
    """Create a GetItemsRequest for the Amazon API."""
    try:
        return GetItemsRequest(
            resources=_get_request_resources(GetItemsResource),
            partner_type=PartnerType.ASSOCIATES,
            marketplace=amazon_api.marketplace,
            partner_tag=amazon_api.tag,
            item_ids=asin_chunk,
            **kwargs,
        )
    except TypeError as exc:
        msg = f"Parameters for get_items request are not correct: {exc}"
        raise MalformedRequest(msg) from exc


def get_items_response(amazon_api: AmazonApi, request: GetItemsRequest) -> list[Item]:
    """Execute a GetItemsRequest and return the list of items."""
    try:
        response = amazon_api.api.get_items(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.items_result is None:
        msg = "No items have been found"
        raise ItemsNotFound(msg)

    return cast(List[Item], response.items_result.items)


def get_search_items_request(
    amazon_api: AmazonApi,
    **kwargs: Any,
) -> SearchItemsRequest:
    """Create a SearchItemsRequest for the Amazon API."""
    try:
        return SearchItemsRequest(
            resources=_get_request_resources(SearchItemsResource),
            partner_type=PartnerType.ASSOCIATES,
            marketplace=amazon_api.marketplace,
            partner_tag=amazon_api.tag,
            **kwargs,
        )
    except TypeError as exc:
        msg = f"Parameters for search_items request are not correct: {exc}"
        raise MalformedRequest(msg) from exc


def get_search_items_response(
    amazon_api: AmazonApi, request: SearchItemsRequest
) -> SearchResult:
    """Execute a SearchItemsRequest and return the search result."""
    try:
        response = amazon_api.api.search_items(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.search_result is None:
        msg = "No items have been found"
        raise ItemsNotFound(msg)

    return cast(SearchResult, response.search_result)


def get_variations_request(
    amazon_api: AmazonApi,
    **kwargs: Any,
) -> GetVariationsRequest:
    """Create a GetVariationsRequest for the Amazon API."""
    try:
        return GetVariationsRequest(
            resources=_get_request_resources(GetVariationsResource),
            partner_type=PartnerType.ASSOCIATES,
            marketplace=amazon_api.marketplace,
            partner_tag=amazon_api.tag,
            **kwargs,
        )
    except TypeError as exc:
        msg = f"Parameters for get_variations request are not correct: {exc}"
        raise MalformedRequest(msg) from exc


def get_variations_response(
    amazon_api: AmazonApi, request: GetVariationsRequest
) -> VariationsResult:
    """Execute a GetVariationsRequest and return the variations result."""
    try:
        response = amazon_api.api.get_variations(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.variations_result is None:
        msg = "No variation items have been found"
        raise ItemsNotFound(msg)

    return cast(VariationsResult, response.variations_result)


def get_browse_nodes_request(
    amazon_api: AmazonApi,
    **kwargs: Any,
) -> GetBrowseNodesRequest:
    """Create a GetBrowseNodesRequest for the Amazon API."""
    try:
        return GetBrowseNodesRequest(
            resources=_get_request_resources(GetBrowseNodesResource),
            partner_type=PartnerType.ASSOCIATES,
            marketplace=amazon_api.marketplace,
            partner_tag=amazon_api.tag,
            **kwargs,
        )
    except TypeError as exc:
        msg = f"Parameters for get_browse_nodes request are not correct: {exc}"
        raise MalformedRequest(msg) from exc


def get_browse_nodes_response(
    amazon_api: AmazonApi, request: GetBrowseNodesRequest
) -> list[BrowseNode]:
    """Execute a GetBrowseNodesRequest and return the list of browse nodes."""
    try:
        response = amazon_api.api.get_browse_nodes(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.browse_nodes_result is None:
        msg = "No browse nodes have been found"
        raise ItemsNotFound(msg)

    return cast(List[BrowseNode], response.browse_nodes_result.browse_nodes)


def _get_request_resources(resource_class: type[object]) -> list[str]:
    """Extract all resource strings from a resource class."""
    members = inspect.getmembers(resource_class, lambda a: not inspect.isroutine(a))
    return [x[-1] for x in members if isinstance(x[-1], str) and x[0][0:2] != "__"]


def _manage_response_exceptions(error: ApiExceptionType) -> NoReturn:
    """Handle API exceptions and raise appropriate custom exceptions."""
    error_status = getattr(error, "status", None)
    error_body = getattr(error, "body", "") or ""

    if error_status == 429:
        msg = (
            "Requests limit reached, try increasing throttling or wait before"
            " trying again"
        )
        raise TooManyRequests(msg)

    if "InvalidParameterValue" in error_body:
        msg = "The value provided in the request for atleast one parameter is invalid."
        raise InvalidArgument(msg)

    if "InvalidPartnerTag" in error_body:
        msg = "The partner tag is invalid or not present."
        raise InvalidArgument(msg)

    if "InvalidAssociate" in error_body:
        msg = "Used credentials are not valid for the selected country."
        raise AssociateValidationError(msg)

    raise RequestError("Request failed: " + str(error.reason))
