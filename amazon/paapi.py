"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
This module allows to get product information from Amazon using the official API in
an easier way.
"""

from .paapi5_python_sdk.api.default_api import DefaultApi
from .paapi5_python_sdk.get_items_request import GetItemsRequest
from .paapi5_python_sdk.search_items_request import SearchItemsRequest
from .paapi5_python_sdk.get_variations_request import GetVariationsRequest
from .paapi5_python_sdk.get_browse_nodes_request import GetBrowseNodesRequest
from .paapi5_python_sdk.partner_type import PartnerType
from .paapi5_python_sdk.rest import ApiException

from amazon.constant import DOMAINS, REGIONS, CONDITION
from amazon.constant import PRODUCT_RESOURCES, SEARCH_RESOURCES, VARIATION_RESOURCES
from amazon.constant import BROWSE_RESOURCES
from amazon.exception import AmazonException
from amazon.parse import parse_product, AmazonBrowseNode, parse_browsenode
from amazon.tools import get_asin, chunks

import logging
import time


logger = logging.getLogger(__name__)


class AmazonAPI:
    """Creates an instance containing your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        tag (str): The tag you want to use for the URL.
        country (str): Country code. Use one of the following:
            AU, BR, CA, FR, DE, IN, NL, IT, JP, MX, ES, TR, AE, UK, US, SE.
        throttling (float, optional): It should be greater than 0 or False to disable throttling.
        This value determines wait time between API calls.
    """
    def __init__(self, key, secret, tag, country, throttling=0.8):
        logger.warning('This version of the module is deprecated and it will be removed in future updates. Please upgrade to version 4.0.0 or higher.')
        self.key = key
        self.secret = secret
        self.tag = tag
        try:
            if throttling is True:
                raise ValueError
            elif throttling is False:
                self.throttling = False
            else:
                self.throttling = float(throttling)
                if self.throttling <= 0:
                    raise ValueError
        except ValueError:
            raise AmazonException('ValueError', 'Throttling should be False or greater than 0')
        self.country = country
        try:
            self.host = 'webservices.amazon.' + DOMAINS[country]
            self.region = REGIONS[country]
            self.marketplace = 'www.amazon.' + DOMAINS[country]
        except KeyError:
            raise AmazonException('KeyError', 'Invalid country code')
        self.last_query_time = time.time()
        self.api = DefaultApi(access_key=self.key, secret_key=self.secret, host=self.host,
                              region=self.region)

    def _throttle(self):
        if self.throttling:
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
        self.last_query_time = time.time()

    def get_products(self, product_ids, condition='Any', merchant='All',
                     async_req=False):
        """Find product information for multiple products on Amazon.

        Args:
            product_ids (str|list): One or more item IDs like ASIN or product URL.
                Use a string separated by comma or as a list.
            condition (str, optional): Specify the product condition.
                Allowed values: Any, Collectible, New, Refurbished, Used.
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

        logger.warning('This version of the module is deprecated and it will be removed in future updates. Please upgrade to version 4.0.0 or higher.')
        # Clean up input data and remove 10 items limit from Amazon API
        if isinstance(product_ids, str):
            product_ids = [x.strip() for x in product_ids.split(',')]
        elif not isinstance(product_ids, list):
            raise AmazonException('TypeError', 'Arg product_ids should be a list or string')
        asin_full_list = list(set([get_asin(x) for x in product_ids]))
        asin_full_list = list(chunks(asin_full_list, 10))

        results = []
        for asin_list in asin_full_list:
            try:
                request = GetItemsRequest(partner_tag=self.tag,
                                          partner_type=PartnerType.ASSOCIATES,
                                          marketplace=self.marketplace,
                                          merchant=merchant,
                                          condition=CONDITION[condition],
                                          item_ids=asin_list,
                                          resources=PRODUCT_RESOURCES)
            except KeyError:
                raise AmazonException('KeyError', 'Invalid condition value')
            except Exception as e:
                raise AmazonException('GetItemsError', e)

            for x in range(3):
                try:
                    # Send the request and create results
                    self._throttle()
                    if async_req:
                        thread = self.api.get_items(request, async_req=True)
                        response = thread.get()
                    else:
                        response = self.api.get_items(request)
                    break
                except ApiException as e:
                    if x == 2:
                        raise AmazonException('ApiException', e)
            try:
                if response.items_result is not None:
                    if len(response.items_result.items) > 0:
                        for item in response.items_result.items:
                            results.append(parse_product(item))
            except Exception as e:
                raise AmazonException('ResponseError', e)

        if results:
            return results
        else:
            return None

    def get_product(self, product_id, condition='Any', merchant='All',
                    async_req=False):
        """Find product information for a specific product on Amazon.

        Args:
            product_id (str, list): One item ID like ASIN or product URL.
            condition (str, optional): Specify the product condition.
                Allowed values: Any, Collectible, New, Refurbished, Used.
                Defaults to Any.
            merchant (str, optional): Filters search results to return items
                having at least one offer sold by target merchant. Allowed values:
                All, Amazon. Defaults to All.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            instance: An instance containing all the available information
                for the product or None if no results.
        """
        if isinstance(product_id, list):
            product_id = product_id[0]
        if isinstance(product_id, str):
            product_id = product_id.split(',')[0]

        product = self.get_products(product_id, condition=condition, merchant=merchant,
                                    async_req=async_req)
        if product:
            return product[0]
        else:
            return None

    def search_products(self, item_count=10, item_page=1, items_per_page=10, keywords=None,
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

        logger.warning('This version of the module is deprecated and it will be removed in future updates. Please upgrade to version 4.0.0 or higher.')
        if items_per_page > 10 or items_per_page < 1:
            raise AmazonException('ValueError', 'Arg items_per_page should be between 1 and 10')
        if item_count > 100 or item_count < 1:
            raise AmazonException('ValueError', 'Arg item_count should be between 1 and 100')
        if item_page < 1:
            raise AmazonException('ValueError', 'Arg item_page should be 1 or higher')
        if not keywords and not actor and not artist and not author and not brand and not title and not browse_node and not search_index:
            raise AmazonException('ValueError', 'At least one of the following args must be '
                                                'provided: keywords, actor, artist, author, brand, '
                                                'title, browse_node, search_index')
        results = []
        while len(results) < item_count:
            try:
                request = SearchItemsRequest(
                    partner_tag=self.tag,
                    partner_type=PartnerType.ASSOCIATES,
                    actor=actor,
                    artist=artist,
                    author=author,
                    availability=availability,
                    brand=brand,
                    browse_node_id=browse_node,
                    condition=CONDITION[condition],
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
                    resources=SEARCH_RESOURCES,
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
                        thread = self.api.search_items(request, async_req=True)
                        response = thread.get()
                    else:
                        response = self.api.search_items(request)
                    break
                except ApiException as e:
                    if x == 2:
                        raise AmazonException('ApiException', e)
            try:
                if response.search_result is not None:
                    if response.search_result.items is not None:
                        for item in response.search_result.items:
                            results.append(parse_product(item))
                            if len(results) >= item_count:
                                break
                        if len(response.search_result.items) < items_per_page:
                            break
                else:
                    break
                if response.errors is not None:
                    raise AmazonException(response.errors[0].code, response.errors[0].message)
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

        logger.warning('This version of the module is deprecated and it will be removed in future updates. Please upgrade to version 4.0.0 or higher.')
        if items_per_page > 10 or items_per_page < 1:
            raise AmazonException('ValueError', 'Arg items_per_page should be between 1 and 10')
        if item_count > 100 or item_count < 1:
            raise AmazonException('ValueError', 'Arg item_count should be between 1 and 100')
        if item_page < 1:
            raise AmazonException('ValueError', 'Arg item_page should be 1 or higher')

        results = []
        while len(results) < item_count:
            try:
                request = GetVariationsRequest(
                    partner_tag=self.tag,
                    partner_type=PartnerType.ASSOCIATES,
                    marketplace=self.marketplace,
                    asin=get_asin(asin),
                    condition=CONDITION[condition],
                    merchant=merchant,
                    offer_count=1,
                    variation_count=items_per_page,
                    variation_page=item_page,
                    resources=VARIATION_RESOURCES)
            except KeyError:
                raise AmazonException('KeyError', 'Invalid condition value')
            except Exception as e:
                raise AmazonException('GetVariationsError', e)

            for x in range(3):
                try:
                    # Send the request and create results
                    self._throttle()
                    if async_req:
                        thread = self.api.get_variations(request, async_req=True)
                        response = thread.get()
                    else:
                        response = self.api.get_variations(request)
                    break
                except ApiException as e:
                    if x == 2:
                        raise AmazonException('ApiException', e)
            try:
                if response.variations_result is not None:
                    if response.variations_result.items is not None:
                        for item in response.variations_result.items:
                            results.append(parse_product(item))
                            if len(results) >= item_count:
                                break
                        if len(response.variations_result.items) < items_per_page:
                            break
                else:
                    break
                if response.errors is not None:
                    raise AmazonException(response.errors[0].code, response.errors[0].message)
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

        logger.warning('This version of the module is deprecated and it will be removed in future updates. Please upgrade to version 4.0.0 or higher.')
        if isinstance(browse_nodes, list) is False:
            raise Exception('Browse nodes parameter should be a list')
        elif not browse_nodes:
            raise Exception('Browse nodes parameter can\'t be empty')

        try:
            request = GetBrowseNodesRequest(
                partner_tag=self.tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace=self.marketplace,
                browse_node_ids=browse_nodes,
                languages_of_preference=None,
                resources=BROWSE_RESOURCES)
        except ValueError as e:
            raise AmazonException("ValueError", e)

        try:
            self._throttle()
            if async_req:
                thread = self.api.get_browse_nodes(request, async_req=True)
                response = thread.get()
            else:
                response = self.api.get_browse_nodes(request)
        except ApiException as e:
            raise AmazonException('ApiException', e)

        try:
            if response.browse_nodes_result is not None:
                res = [AmazonBrowseNode(item) for item in response.browse_nodes_result.browse_nodes]
                return parse_browsenode(res)
            if response.errors is not None:
                raise AmazonException(response.errors[0].code, response.errors[0].message)
        except TypeError as e:
            raise AmazonException("TypeError", e)
        except ValueError as e:
            raise AmazonException(ValueError, e)
        except AmazonException as e:
            raise AmazonException(e.status, e.reason)
        except Exception as e:
            raise AmazonException("General", e)
