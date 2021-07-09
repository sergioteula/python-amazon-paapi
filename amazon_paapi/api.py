"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
This module allows to get product information from Amazon using the official API in
an easier way.
"""

from .sdk.api.default_api import DefaultApi
from .sdk.models.get_browse_nodes_request import GetBrowseNodesRequest
from .sdk.models.partner_type import PartnerType
from .sdk.rest import ApiException

from . import models
from .helpers.arguments import check_search_args, check_variations_args, get_items_ids
from .helpers.requests import get_items_request, get_items_response, get_search_items_request, get_search_items_response
from .helpers.generators import get_list_chunks
from .errors import AmazonException, InvalidArgumentException
from .tools import get_asin

from typing import Union
import time


class AmazonApi:
    """Provides methods to get information from Amazon using your API credentials.

    Args:
        key (``str``): Your API key.
        secret (``str``): Your API secret.
        tag (``str``): Your affiliate tracking id, used to create the affiliate link.
        country (``models.Country``): Country code for your affiliate account.
        throttling (``float``, optional): Wait time in seconds between API calls. Use it to avoid
            reaching Amazon limits. Defaults to ``1`` second.

    Raises:
        ``InvalidArgumentException``
    """

    def __init__(self, key: str, secret: str, tag: str, country: models.Country, throttling: float = 1, **kwargs):
        self._key = key
        self._secret = secret
        self._tag = tag
        self._country = country
        self._throttling = float(throttling)
        self._last_query_time = time.time() - throttling

        try:
            self._host = 'webservices.amazon.' + models.DOMAINS[country]
            self._region = models.REGIONS[country]
            self._marketplace = 'www.amazon.' + models.DOMAINS[country]
        except KeyError:
            raise InvalidArgumentException('Country code is not correct')

        self._api = DefaultApi(key, secret, self._host, self._region)


    def get_items(self,
        items: Union[str, list[str]],
        condition: models.Condition = None,
        merchant: models.Merchant = None,
        currency_of_preference: str = None,
        languages_of_preference: list[str] = None,
        **kwargs) -> list[models.ApiItem]:

        """Get items information from Amazon.

        Args:
            items (``str`` | ``list[str]``): One or more items, using ASIN or product URL. Items
                in string format should be separated by commas.
            condition (``models.Condition``, optional): Filters offers by condition type.
                Defaults to ``Any``.
            merchant (``models.Merchant``, optional): Filters search results to return items having
                at least one offer sold by target merchant. Defaults to ``All``.
            currency_of_preference (``str``, optional): Currency of preference in which the prices
                information should be returned. Expected currency code format is ISO 4217.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``list[ApiItem]``: A list of items with Amazon information.

        Raises:
            ``InvalidArgumentException``
            ``MalformedRequestException``
            ``ApiRequestException``
            ``ItemsNotFoudException``
        """

        kwargs.update({
            'condition': condition,
            'merchant': merchant,
            'currency_of_preference': currency_of_preference,
            'languages_of_preference': languages_of_preference
            })

        items_ids = get_items_ids(items)
        results = []

        for asin_chunk in get_list_chunks(items_ids, chunk_size=10):
            request = get_items_request(self, asin_chunk, **kwargs)
            self._throttle()
            items_response = get_items_response(self, request)
            results.extend(items_response)

        return results


    def search_items(self,
        item_count: int = None,
        item_page: int = None,
        actor: str = None,
        artist: str = None,
        author: str = None,
        brand: str = None,
        keywords: str = None,
        title: str = None,
        availability: models.Availability = None,
        browse_node_id: str = None,
        condition: models.Condition = None,
        currency_of_preference: str = None,
        delivery_flags: list[str] = None,
        languages_of_preference: list[str] = None,
        merchant: models.Merchant = None,
        max_price: int = None,
        min_price: int = None,
        min_saving_percent: int = None,
        min_reviews_rating: int = None,
        search_index: str = None,
        sort_by: models.SortBy = None,
        **kwargs) -> list[models.ApiItem]:
        """Searches for items on Amazon based on a search query. At least one of the following
        parameters should be specified: ``keywords``, ``actor``, ``artist``, ``author``,
        ``brand`` or ``title``.

        Args:
            item_count (``int``, optional): Number of items returned. Should be between ``1`` and ``10``.
                Defaults to ``10``.
            item_page (``int``, optional): The specific page of items to be returned from the available
                results. Should be between ``1`` and ``10``. Defaults to ``1``.
            actor (``str``, optional): Actor name associated with the item.
            artist (``str``, optional): Artist name associated with the item.
            author (``str``, optional): Author name associated with the item.
            brand (``str``, optional): Brand name associated with the item.
            keywords (``str``, optional): A word or phrase that describes an item.
            title (``str``, optional): Title associated with the item.
            availability (``models.Availability``, optional): Filters available items on Amazon.
                Defaults to ``Available``.
            browse_node_id (``str``, optional): A unique ID assigned by Amazon that identifies a product
                category or subcategory.
            condition (``models.Condition``, optional): Filters offers by condition type. Defaults to ``Any``.
            currency_of_preference (``str``, optional): Currency of preference in which the prices
                information should be returned. Expected currency code format is ISO 4217.
            delivery_flags (``list[str]``): Filters items which satisfy a certain delivery program.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            merchant (``models.Merchant``, optional): Filters search results to return items having
                at least one offer sold by target merchant. Defaults to ``All``.
            max_price (``int``, optional): Filters search results to items with at least one offer price
                below the specified value. Prices appear in lowest currency denomination.
                For example, $31.41 should be passed as ``3141`` or 28.00€ should be ``2800``.
            min_price (``int``, optional): Filters search results to items with at least one offer price
                above the specified value. Prices appear in lowest currency denomination.
                For example, $31.41 should be passed as ``3141`` or 28.00€ should be ``2800``.
            min_saving_percent (``int``, optional): Filters search results to items with at least one
                offer having saving percentage above the specified value. Value should be
                ``positive integer less than 100``.
            min_reviews_rating (``int``, optional): Filters search results to items with customer review
                ratings above specified value. Value should be ``positive integer less than 5``.
            search_index (``str``, optional): Indicates the product category to search. Defaults to ``All``.
            sort_by (``models.SortBy``, optional): The way in which items are sorted.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``list[ApiItem]``: A list of items with Amazon information.

        Raises:
            ``InvalidArgumentException``
            ``MalformedRequestException``
            ``ApiRequestException``
            ``ItemsNotFoudException``
        """

        kwargs.update({
            'item_count': item_count,
            'item_page': item_page,
            'actor': actor,
            'artist': artist,
            'author': author,
            'brand': brand,
            'keywords': keywords,
            'title': title,
            'availability': availability,
            'browse_node_id': browse_node_id,
            'condition': condition,
            'currency_of_preference': currency_of_preference,
            'delivery_flags': delivery_flags,
            'languages_of_preference': languages_of_preference,
            'max_price': max_price,
            'merchant': merchant,
            'min_price': min_price,
            'min_reviews_rating': min_reviews_rating,
            'min_saving_percent': min_saving_percent,
            'search_index': search_index,
            'sort_by': sort_by,
        })

        check_search_args(**kwargs)
        request = get_search_items_request(self, **kwargs)
        self._throttle()
        return get_search_items_response(self, request)


    def get_variations(self,
        asin: str,
        variation_count: int = None,
        variation_page: int = None,
        condition: models.Condition = None,
        currency_of_preference: str = None,
        merchant: models.Merchant = None,
        **kwargs) -> list[models.ApiItem]:
        """Returns a set of items that are the same product, but differ according to a
        consistent theme, for example size and color.

        Args:
            asin (str): One item ID like ASIN or product URL.
            item_count (int, optional): The total number of products to get. Should be between
                1 and 100. Defaults to 10.
            item_page (int, optional): The page where the results start from. Should be between
                1 and 10. Defaults to 1.
            items_per_page (int, optional): Products on each page. Should be between
                1 and 10. Defaults to 10.
            condition (str, optional): The condition parameter filters offers by
                condition type. Allowed values: Any, Collectible, New, Refurbished, Used.
                Defaults to Any.
            merchant (str, optional): Filters search results to return items
                having at least one offer sold by target merchant. Allowed values:
                All, Amazon. Defaults to All.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            list of instances: A list containing 1 instance for each product
                or None if no results.
        """

        kwargs.update({
            'asin': asin,
            'variation_count': variation_count,
            'variation_page': variation_page,
            'condition': condition,
            'currency_of_preference': currency_of_preference,
            'merchant': merchant
        })

        check_variations_args(**kwargs)
        request = get_variations_request(self, **kwargs)
        self._throttle()
        return get_variations_response(self, request)

        # if items_per_page > 10 or items_per_page < 1:
        #     raise AmazonException(
        #         'ValueError', 'Arg items_per_page should be between 1 and 10')
        # if item_count > 100 or item_count < 1:
        #     raise AmazonException(
        #         'ValueError', 'Arg item_count should be between 1 and 100')
        # if item_page < 1:
        #     raise AmazonException(
        #         'ValueError', 'Arg item_page should be 1 or higher')

        # results = []
        # while len(results) < item_count:
        #     try:
        #         request = GetVariationsRequest(
        #             partner_tag=self._tag,
        #             partner_type=PartnerType.ASSOCIATES,
        #             marketplace=self._marketplace,
        #             asin=get_asin(asin),
        #             condition=models.CONDITION[condition],
        #             merchant=merchant,
        #             offer_count=1,
        #             variation_count=items_per_page,
        #             variation_page=item_page,
        #             resources=models.VARIATION_RESOURCES)
        #     except KeyError:
        #         raise AmazonException('KeyError', 'Invalid condition value')
        #     except Exception as e:
        #         raise AmazonException('GetVariationsError', e)

        #     for x in range(3):
        #         try:
        #             # Send the request and create results
        #             self._throttle()
        #             if async_req:
        #                 thread = self._api.get_variations(
        #                     request, async_req=True)
        #                 response = thread.get()
        #             else:
        #                 response = self._api.get_variations(request)
        #             break
        #         except ApiException as e:
        #             if x == 2:
        #                 raise AmazonException('ApiException', e)
        #     try:
        #         if response.variations_result is not None:
        #             if response.variations_result.items is not None:
        #                 for item in response.variations_result.items:
        #                     results.append(get_parsed_item(item))
        #                     if len(results) >= item_count:
        #                         break
        #                 if len(response.variations_result.items) < items_per_page:
        #                     break
        #         else:
        #             break
        #         if response.errors is not None:
        #             raise AmazonException(
        #                 response.errors[0].code, response.errors[0].message)
        #     except Exception as e:
        #         raise AmazonException('ResponseError', e)
        #     item_page += 1

        # if results:
        #     return results
        # else:
        #     return None

    def get_browsenodes(self, browse_nodes, async_req=False):
        """Get browse nodes information from Amazon.

        Args:
            browse_nodes (list): List of strings containing the browse node ids.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            dict: A dictionary containing the browse node information.
        """

        if isinstance(browse_nodes, list) is False:
            raise Exception('Browse nodes parameter should be a list')
        elif not browse_nodes:
            raise Exception('Browse nodes parameter can\'t be empty')

        try:
            request = GetBrowseNodesRequest(
                partner_tag=self._tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self._marketplace,
                browse_node_ids=browse_nodes,
                languages_of_preference=None,
                resources=models.BROWSE_RESOURCES)
        except ValueError as e:
            raise AmazonException("ValueError", e)

        try:
            self._throttle()
            if async_req:
                thread = self._api.get_browse_nodes(request, async_req=True)
                response = thread.get()
            else:
                response = self._api.get_browse_nodes(request)
        except ApiException as e:
            raise AmazonException('ApiException', e)

        try:
            if response.browse_nodes_result is not None:
                res = [AmazonBrowseNode(
                    item) for item in response.browse_nodes_result.browse_nodes]
                return parse_browsenode(res)
            if response.errors is not None:
                raise AmazonException(
                    response.errors[0].code, response.errors[0].message)
        except TypeError as e:
            raise AmazonException("TypeError", e)
        except ValueError as e:
            raise AmazonException(ValueError, e)
        except AmazonException as e:
            raise AmazonException(e.status, e.reason)
        except Exception as e:
            raise AmazonException("General", e)

    def _throttle(self):
        wait_time = self._throttling - (time.time() - self._last_query_time)
        if wait_time > 0:
            time.sleep(wait_time)
        self._last_query_time = time.time()
