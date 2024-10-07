"""Module with helper functions for creating requests."""

import inspect
from typing import List

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


def get_items_request(amazon_api, asin_chunk: List[str], **kwargs) -> GetItemsRequest:
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


def get_items_response(amazon_api, request: GetItemsRequest) -> List[Item]:
    try:
        response = amazon_api.api.get_items(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.items_result is None:
        msg = "No items have been found"
        raise ItemsNotFound(msg)

    return response.items_result.items


def get_search_items_request(amazon_api, **kwargs) -> SearchItemsRequest:
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


def get_search_items_response(amazon_api, request: SearchItemsRequest) -> SearchResult:
    try:
        response = amazon_api.api.search_items(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.search_result is None:
        msg = "No items have been found"
        raise ItemsNotFound(msg)

    return response.search_result


def get_variations_request(amazon_api, **kwargs) -> GetVariationsRequest:
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
    amazon_api, request: GetVariationsRequest
) -> VariationsResult:
    try:
        response = amazon_api.api.get_variations(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.variations_result is None:
        msg = "No variation items have been found"
        raise ItemsNotFound(msg)

    return response.variations_result


def get_browse_nodes_request(amazon_api, **kwargs) -> GetBrowseNodesRequest:
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
    amazon_api, request: GetBrowseNodesRequest
) -> List[BrowseNode]:
    try:
        response = amazon_api.api.get_browse_nodes(request)
    except ApiException as exc:
        _manage_response_exceptions(exc)

    if response.browse_nodes_result is None:
        msg = "No browse nodes have been found"
        raise ItemsNotFound(msg)

    return response.browse_nodes_result.browse_nodes


def _get_request_resources(resources) -> List[str]:
    resources = inspect.getmembers(resources, lambda a: not inspect.isroutine(a))
    return [x[-1] for x in resources if isinstance(x[-1], str) and x[0][0:2] != "__"]


def _manage_response_exceptions(error) -> None:
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
