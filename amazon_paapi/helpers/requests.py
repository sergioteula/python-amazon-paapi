"""Module with helper functions for creating requests."""


from .. import models
from ..errors import ApiRequestException, ItemsNotFoudException, MalformedRequestException
from ..sdk.models.get_items_resource import GetItemsResource
from ..sdk.models.get_items_request import GetItemsRequest
from ..sdk.models.search_items_resource import SearchItemsResource
from ..sdk.models.search_items_request import SearchItemsRequest
from ..sdk.rest import ApiException
import inspect


def get_items_request(self, asin_chunk: list[str], **kwargs) -> models.GetItemsRequest:
    try:
        return GetItemsRequest(resources=_get_request_resources(GetItemsResource),
                               partner_type=models.PartnerType.ASSOCIATES,
                               marketplace=self._marketplace,
                               partner_tag=self._tag,
                               item_ids=asin_chunk,
                               **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for get_items request are not correct: ' + str(e))


def get_items_response(self, request: models.GetItemsRequest) -> list[models.ApiItem]:
    try:
        response = self._api.get_items(request)
    except ApiException as e:
        raise ApiRequestException('Error getting a response from Amazon API: ' + str(e))

    if response.items_result == None:
        raise ItemsNotFoudException('No items have been found')

    return response.items_result.items


def get_search_items_request(self, **kwargs) -> models.SearchItemsResource:
    try:
        return SearchItemsRequest(resources=_get_request_resources(SearchItemsResource),
                               partner_type=models.PartnerType.ASSOCIATES,
                               marketplace=self._marketplace,
                               partner_tag=self._tag,
                               **kwargs)
    except TypeError as e:
        raise MalformedRequestException('Parameters for search_items request are not correct: ' + str(e))


def get_search_items_response(self, request: models.SearchItemsRequest) -> list[models.ApiItem]:
    try:
        response = self._api.search_items(request)
    except ApiException as e:
        raise ApiRequestException('Error getting a response from Amazon API: ' + str(e))

    if response.search_result == None:
        raise ItemsNotFoudException('No items have been found')

    return response.search_result.items


def _get_request_resources(resources) -> list[str]:
    resources = inspect.getmembers(resources, lambda a:not(inspect.isroutine(a)))
    resources = [x[-1] for x in resources if isinstance(x[-1], str) and x[0][0:2] != '__']
    return resources
