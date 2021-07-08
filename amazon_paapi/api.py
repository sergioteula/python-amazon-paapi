"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
This module allows to get product information from Amazon using the official API in
an easier way.
"""

from .sdk.api.default_api import DefaultApi
from .sdk.models.search_items_request import SearchItemsRequest
from .sdk.models.get_variations_request import GetVariationsRequest
from .sdk.models.get_browse_nodes_request import GetBrowseNodesRequest
from .sdk.models.partner_type import PartnerType
from .sdk.rest import ApiException

from . import models
from .helpers.arguments import get_items_ids
from .helpers.requests import get_items_request, get_items_response
from .helpers.generators import get_list_chunks
from .exceptions import AmazonException, InvalidArgumentException
from .tools import get_asin

from typing import Union
import time


class AmazonApi:
    """Provides methods to get information from Amazon using your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        tag (str): Your affiliate tracking id, used to create the affiliate link.
        country (str): Country code for your affiliate account. Available values in models.Country.
        throttling (float, optional): Wait time in seconds between API calls. Use it to avoid
            reaching Amazon limits. Defaults to 1 second.
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
        Full official documentation [here](https://webservices.amazon.com/paapi5/documentation/get-items.html#ItemLookup-rp).

        Args:
            items (str | list[str]): One or more items using ASIN or product URL. Use a string
                separated by comma or a list of strings.
            condition (str, optional): The condition parameter filters offers by condition type.
                Available values in models.Condition. Defaults to Any.
            merchant (str, optional): Filters search results to return items having at least one
                offer sold by target merchant. Available values in models.Merchant. Defaults to All.
            currency_of_preference (str, optional): Currency of preference in which the prices
                information should be returned in response. By default the prices are returned
                in the default currency of the marketplace. Expected currency code format is
                ISO 4217.
            languages_of_preference (list[str], optional): Languages in order of preference in
                which the item information should be returned in response. By default the item
                information is returned in the default language of the marketplace.
            kwargs (any): Any other parameters supported by Amazon API for the GetItems operation.

        Returns:
            list[AmazonItem]: A list of items with Amazon information.
        """

        kwargs.update({
            'condition': condition,
            'merchant': merchant,
            'currency_of_preference': currency_of_preference,
            'languages_of_preference': languages_of_preference
            })

        items_ids = get_items_ids(items)
        results = []

        for asin_chunk in get_list_chunks(items_ids, 10):
            request = get_items_request(self, asin_chunk, **kwargs)
            self._throttle()
            items_response = get_items_response(self, request)
            results.extend(items_response)

        return results

    def search_items(self, item_count=10, item_page=1, items_per_page=10, keywords=None,
                        actor=None, artist=None, author=None, brand=None, title=None,
                        availability='Available', browse_node=None, condition='Any', delivery=None,
                        max_price=None, min_price=None, min_rating=None, min_discount=None,
                        merchant='All', search_index='All', sort_by=None, async_req=False):
        """Search products on Amazon using different parameters. At least one of the
        following parameters should be used: keywords, actor, artist, author, brand,
        title.

        Args:
            item_count (int, optional): The total number of products to get. Should be between
                1 and 100. Defaults to 10.
            item_page (int, optional): The page where the results start from. Should be between
                1 and 10. Defaults to 1.
            items_per_page (int, optional): Products on each page. Should be between
                1 and 10. Defaults to 10.
            keywords (str, optional): A word or phrase that describes an item.
            actor (str, optional): Actor name associated with the item.
            artist (str, optional): Artist name associated with the item.
            author (str, optional): Author name associated with the item.
            brand (str, optional): Brand name associated with the item.
            title (str, optional): Title associated with the item.
            availability (str, optional): Filters available items on Amazon. Allowed values:
            Available, IncludeOutOfStock. Defaults to Available.
            browse_node (str, optional): A unique ID assigned by Amazon that
                identifies a product category or subcategory.
            condition (str, optional): The condition parameter filters offers by
                condition type. Allowed values: Any, Collectible, New, Refurbished, Used.
                Defaults to Any.
            delivery (list, optional): The delivery flag filters items which
                satisfy a certain delivery program promoted by the specific
                Amazon Marketplace. Allowed values: AmazonGlobal, FreeShipping,
                FulfilledByAmazon, Prime.
            max_price (int, optional): Filters search results to items with at
                least one offer price below the specified value.
            min_price (int, optional): Filters search results to items with at
                least one offer price above the specified value.
            min_rating (int, optional): Filters search results to items with
                customer review ratings above specified value.
            min_discount (int, optional): Filters search results to items with
                at least one offer having saving percentage above the specified
                value.
            merchant (str, optional): Filters search results to return items
                having at least one offer sold by target merchant. Allowed values:
                All, Amazon. Defaults to All.
            search_index (str, optional): Indicates the product category to
                search. Defaults to All.
            sort_by (str, optional): The way in which items in the response
                are sorted. Allowed values: AvgCustomerReviews, Featured,
                NewestArrivals, Price:HighToLow, Price:LowToHigh, Relevance.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            list of instances: A list containing 1 instance for each product
                or None if no results.
        """
        if items_per_page > 10 or items_per_page < 1:
            raise AmazonException(
                'ValueError', 'Arg items_per_page should be between 1 and 10')
        if item_count > 100 or item_count < 1:
            raise AmazonException(
                'ValueError', 'Arg item_count should be between 1 and 100')
        if item_page < 1:
            raise AmazonException(
                'ValueError', 'Arg item_page should be 1 or higher')
        if not keywords and not actor and not artist and not author and not brand and not title and not browse_node and not search_index:
            raise AmazonException('ValueError', 'At least one of the following args must be '
                                                'provided: keywords, actor, artist, author, brand, '
                                                'title, browse_node, search_index')
        results = []
        while len(results) < item_count:
            try:
                request = SearchItemsRequest(
                    partner_tag=self._tag,
                    partner_type=PartnerType.ASSOCIATES,
                    actor=actor,
                    artist=artist,
                    author=author,
                    availability=availability,
                    brand=brand,
                    browse_node_id=browse_node,
                    condition=models.CONDITION[condition],
                    delivery_flags=delivery,
                    item_count=items_per_page,
                    item_page=item_page,
                    keywords=keywords,
                    max_price=max_price,
                    merchant=merchant,
                    min_price=min_price,
                    min_reviews_rating=min_rating,
                    min_saving_percent=min_discount,
                    offer_count=1,
                    resources=models.SEARCH_RESOURCES,
                    search_index=search_index,
                    sort_by=sort_by,
                    title=title)
            except KeyError:
                raise AmazonException('KeyError', 'Invalid condition value')
            except Exception as e:
                raise AmazonException('SearchItemsError', e)

            for x in range(3):
                try:
                    # Send the request and create results
                    self._throttle()
                    if async_req:
                        thread = self._api.search_items(request, async_req=True)
                        response = thread.get()
                    else:
                        response = self._api.search_items(request)
                    break
                except ApiException as e:
                    if x == 2:
                        raise AmazonException('ApiException', e)
            try:
                if response.search_result is not None:
                    if response.search_result.items is not None:
                        for item in response.search_result.items:
                            results.append(get_parsed_item(item))
                            if len(results) >= item_count:
                                break
                        if len(response.search_result.items) < items_per_page:
                            break
                else:
                    break
                if response.errors is not None:
                    raise AmazonException(
                        response.errors[0].code, response.errors[0].message)
            except Exception as e:
                if e.status == "NoResults":
                    break
                raise AmazonException('ResponseError', e)
            item_page += 1

        if results:
            return results
        else:
            return None

    def get_variations(self, asin, item_count=10, item_page=1, items_per_page=10, condition='Any',
                       merchant='All', async_req=False):
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
        if items_per_page > 10 or items_per_page < 1:
            raise AmazonException(
                'ValueError', 'Arg items_per_page should be between 1 and 10')
        if item_count > 100 or item_count < 1:
            raise AmazonException(
                'ValueError', 'Arg item_count should be between 1 and 100')
        if item_page < 1:
            raise AmazonException(
                'ValueError', 'Arg item_page should be 1 or higher')

        results = []
        while len(results) < item_count:
            try:
                request = GetVariationsRequest(
                    partner_tag=self._tag,
                    partner_type=PartnerType.ASSOCIATES,
                    marketplace=self._marketplace,
                    asin=get_asin(asin),
                    condition=models.CONDITION[condition],
                    merchant=merchant,
                    offer_count=1,
                    variation_count=items_per_page,
                    variation_page=item_page,
                    resources=models.VARIATION_RESOURCES)
            except KeyError:
                raise AmazonException('KeyError', 'Invalid condition value')
            except Exception as e:
                raise AmazonException('GetVariationsError', e)

            for x in range(3):
                try:
                    # Send the request and create results
                    self._throttle()
                    if async_req:
                        thread = self._api.get_variations(
                            request, async_req=True)
                        response = thread.get()
                    else:
                        response = self._api.get_variations(request)
                    break
                except ApiException as e:
                    if x == 2:
                        raise AmazonException('ApiException', e)
            try:
                if response.variations_result is not None:
                    if response.variations_result.items is not None:
                        for item in response.variations_result.items:
                            results.append(get_parsed_item(item))
                            if len(results) >= item_count:
                                break
                        if len(response.variations_result.items) < items_per_page:
                            break
                else:
                    break
                if response.errors is not None:
                    raise AmazonException(
                        response.errors[0].code, response.errors[0].message)
            except Exception as e:
                raise AmazonException('ResponseError', e)
            item_page += 1

        if results:
            return results
        else:
            return None

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
