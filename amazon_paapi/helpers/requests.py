"""Module with helper functions for creating requests."""


from typing import List
from ..models.item_result import Item
from ..models.search_result import SearchResult
from ..models.variations_result import VariationsResult
from ..models.browse_nodes_result import BrowseNode
from ..errors import ApiRequestException, ItemsNotFoudException, MalformedRequestException, TooManyRequestsException, AssociateValidationException, InvalidArgumentException
from ..sdk.models.partner_type import PartnerType
from ..sdk.models.get_items_resource import GetItemsResource
from ..sdk.models.get_items_request import GetItemsRequest
from ..sdk.models.search_items_resource import SearchItemsResource
from ..sdk.models.search_items_request import SearchItemsRequest
from ..sdk.models.get_variations_resource import GetVariationsResource
from ..sdk.models.get_variations_request import GetVariationsRequest
from ..sdk.models.get_browse_nodes_resource import GetBrowseNodesResource
from ..sdk.models.get_browse_nodes_request import GetBrowseNodesRequest
from ..sdk.rest import ApiException
import inspect


def get_items_request(amazon_api, asin_chunk: List[str], **kwargs) -> GetItemsRequest:
    try:
        return GetItemsRequest(resources=_get_request_resources(GetItemsResource),
                               partner_type=PartnerType.ASSOCIATES,
                               marketplace=amazon_api._marketplace,
                               partner_tag=amazon_api._tag,
                               item_ids=asin_chunk,
                               **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for get_items request are not correct: ' + str(e))


def get_items_response(amazon_api, request: GetItemsRequest) -> List[Item]:
    try:
        response = amazon_api._api.get_items(request)
    except ApiException as e:
        _manage_response_exceptions(e)

    if response.items_result == None:
        raise ItemsNotFoudException('No items have been found')

    return response.items_result.items


def get_search_items_request(amazon_api, **kwargs) -> SearchItemsRequest:
    try:
        return SearchItemsRequest(resources=_get_request_resources(SearchItemsResource),
                                  partner_type=PartnerType.ASSOCIATES,
                                  marketplace=amazon_api._marketplace,
                                  partner_tag=amazon_api._tag,
                                  **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for search_items request are not correct: ' + str(e))


def get_search_items_response(amazon_api, request: SearchItemsRequest) -> SearchResult:
    try:
        response = amazon_api._api.search_items(request)
    except ApiException as e:
        _manage_response_exceptions(e)

    if response.search_result == None:
        raise ItemsNotFoudException('No items have been found')

    return response.search_result


def get_variations_request(amazon_api, **kwargs) -> GetVariationsRequest:
    try:
        return GetVariationsRequest(resources=_get_request_resources(GetVariationsResource),
                                    partner_type=PartnerType.ASSOCIATES,
                                    marketplace=amazon_api._marketplace,
                                    partner_tag=amazon_api._tag,
                                    **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for get_variations request are not correct: ' + str(e))


def get_variations_response(amazon_api, request: GetVariationsRequest) -> VariationsResult:
    try:
        response = amazon_api._api.get_variations(request)
    except ApiException as e:
        _manage_response_exceptions(e)

    if response.variations_result == None:
        raise ItemsNotFoudException('No variation items have been found')

    return response.variations_result


def get_browse_nodes_request(amazon_api, **kwargs) -> GetBrowseNodesRequest:
    try:
        return GetBrowseNodesRequest(resources=_get_request_resources(GetBrowseNodesResource),
                                    partner_type=PartnerType.ASSOCIATES,
                                    marketplace=amazon_api._marketplace,
                                    partner_tag=amazon_api._tag,
                                    **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for get_browse_nodes request are not correct: ' + str(e))


def get_browse_nodes_response(amazon_api, request: GetBrowseNodesRequest) -> List[BrowseNode]:
    try:
        response = amazon_api._api.get_browse_nodes(request)
    except ApiException as e:
        _manage_response_exceptions(e)

    if response.browse_nodes_result == None:
        raise ItemsNotFoudException('No browse nodes have been found')

    return response.browse_nodes_result.browse_nodes


def _get_request_resources(resources) -> List[str]:
    resources = inspect.getmembers(resources, lambda a:not(inspect.isroutine(a)))
    resources = [x[-1] for x in resources if isinstance(x[-1], str) and x[0][0:2] != '__']
    return resources

def _manage_response_exceptions(error) -> None:
    if isinstance(error, ApiException):
        if error.status == 429:
            raise TooManyRequestsException('Requests limit reached, try increasing throttling or wait before trying again')

        elif 'InvalidParameterValue' in error.body:
            raise InvalidArgumentException('The value provided in the request for atleast one parameter is invalid.')

        elif 'InvalidPartnerTag' in error.body:
            raise InvalidArgumentException('The partner tag is invalid or not present.')

        elif 'InvalidAssociate' in error.body:
            raise AssociateValidationException('Used credentials are not valid for the selected country.')

    raise ApiRequestException('Request failed: ' + str(error.reason))
