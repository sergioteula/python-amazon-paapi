"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
This module allows to get product information from Amazon using the official API in
an easier way.
"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.search_items_request import SearchItemsRequest
from paapi5_python_sdk.get_variations_request import GetVariationsRequest
from paapi5_python_sdk.get_browse_nodes_request import GetBrowseNodesRequest
from paapi5_python_sdk.partner_type import PartnerType

import time

from constant import DOMAINS, REGIONS, PRODUCT_RESOURCES, SEARCH_RESOURCES, CONDITION
from exception import AmazonException
from parse import parse_product
from tools import get_asin, chunks


class AmazonAPI:
    """Creates an instance containing your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        tag (str): The tag you want to use for the URL.
        country (str): Country code. Use one of the following:
            AU, BR, CA, FR, DE, IN, IT, JP, MX, ES, TR, AE, UK, US.
        throttling (float, optional): Reduce this value to wait longer
            between API calls.
    """
    def __init__(self, key: str, secret: str, tag: str, country: str, throttling=0.9):
        self.key = key
        self.secret = secret
        self.tag = tag
        self.throttling = throttling
        self.country = country
        self.host = 'webservices.amazon.' + DOMAINS[country]
        self.region = REGIONS[country]
        self.marketplace = 'www.amazon.' + DOMAINS[country]
        self.last_query_time = time.time()
        self.api = DefaultApi(access_key=self.key, secret_key=self.secret, host=self.host,
                              region=self.region)

    def get_products(self, product_ids: [str, list], condition='ANY', async_req=False):
        """Find product information for multiple products on Amazon.

        Args:
            product_ids (str|list): One or more item IDs like ASIN or product URL.
                Use a string separated by comma or as a list.
            condition (str, optional): Specify the product condition.
                Allowed values: ANY, COLLECTIBLE, NEW, REFURBISHED, USED.
                Defaults to ANY.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            list of instances: A list containing 1 instance for each product
                or None if no results.
        """

        # Clean up input data and remove 10 items limit from Amazon API
        if isinstance(product_ids, str):
            product_ids = [x.strip() for x in product_ids.split(',')]
        asin_full_list = list(set([get_asin(x) for x in product_ids]))
        asin_full_list = list(chunks(asin_full_list, 10))

        results = []
        for asin_list in asin_full_list:
            try:
                request = GetItemsRequest(partner_tag=self.tag,
                                          partner_type=PartnerType.ASSOCIATES,
                                          marketplace=self.marketplace,
                                          condition=CONDITION[condition],
                                          item_ids=asin_list,
                                          resources=PRODUCT_RESOURCES)
            except Exception as exception:
                raise AmazonException(exception.status, exception.reason)

            try:
                # Wait before doing the request
                wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                self.last_query_time = time.time()

                # Send the request and create results
                if async_req:
                    thread = self.api.get_items(request, async_req=True)
                    response = thread.get()
                else:
                    response = self.api.get_items(request)
                if response.items_result is not None:
                    if len(response.items_result.items) > 0:
                        for item in response.items_result.items:
                            results.append(parse_product(item))
            except Exception as exception:
                raise AmazonException(exception.status, exception.reason)

        if results:
            return results
        else:
            return None

    def get_product(self, product_id: str, condition='ANY', async_req=False):
        """Find product information for a specific product on Amazon.

        Args:
            product_id (str): One item ID like ASIN or product URL.
            condition (str, optional): Specify the product condition.
                Allowed values: ANY, COLLECTIBLE, NEW, REFURBISHED, USED.
                Defaults to ANY.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            instance: An instance containing all the available information
                for the product or None if no results.
        """
        if isinstance(product_id, list):
            raise AmazonException('TypeError', 'Product ID should be string, not list')
        if isinstance(product_id, str):
            check_product_id = product_id.split(',')
            if len(check_product_id) > 1:
                raise AmazonException('ValueError', 'Only 1 product ID is allowed, use '
                                                    'get_products for multiple requests')
        return self.get_products(product_id, condition=condition, async_req=async_req)[0]

    def search_products(self, item_count=10, item_page=1, items_per_page=10, actor=None,
                        artist=None, author=None, availability=None, brand=None, browse_node=None,
                        condition=None, currency=None, delivery=None, keywords=None, languages=None,
                        max_price=None, min_price=None, min_rating=None, min_discount=None,
                        merchant=None, search_index=None, sort_by=None, title=None,
                        async_req=False):
        """Search products on Amazon using different parameters. At least one of the
        following parameters should be used: keywords, actor, artist, author, brand,
        title.

        Args:
            item_count (int, optional): The total number of products to get.
                Defaults to 10.
            item_page (int, optional): The page where the results start from.
                Defaults to 1.
            items_per_page (int, optional): Products on each page. Should be between
                1 and 10. Defaults to 10.
            actor (str, optional): Actor name associated with the item.
            artist (str, optional): Artist name associated with the item.
            author (str, optional): Author name associated with the item.
            availability (str, optional): Filters available items on Amazon. By
                default, all requests returns available items only.
                Allowed values: Available, IncludeOutOfStock.
            brand (str, optional): Brand name associated with the item.
            browse_node (str, optional): A unique ID assigned by Amazon that
                identifies a product category or subcategory.
            condition (str, optional): The condition parameter filters offers by
                condition type. By default, condition equals Any.
                Allowed values: ANY, COLLECTIBLE, NEW, REFURBISHED, USED.
            currency (str, optional): Currency of preference in which the prices
                information should be returned in response.
            delivery (list, optional): The delivery flag filters items which
                satisfy a certain delivery program promoted by the specific
                Amazon Marketplace. Allowed values: AmazonGlobal, FreeShipping,
                FulfilledByAmazon, Prime.
            keywords (str, optional): A word or phrase that describes an item.
            languages (list, optional): Languages in order of preference in which
                the item information should be returned in response.
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
                having at least one offer sold by target merchant. By default
                the value All is passed. Allowed values: All, Amazon.
            search_index (str, optional): Indicates the product category to
                search.
            sort_by (str, optional): The way in which items in the response
                are sorted. Allowed values: AvgCustomerReviews, Featured,
                NewestArrivals, Price:HighToLow, Price:LowToHigh, Relevance.
            title (str, optional): Title associated with the item.
            async_req (bool, optional): Specify if a thread should be created to
                run the request. Defaults to False.

        Returns:
            list of instances: A list containing 1 instance for each product
                or None if no results.
        """
        if items_per_page > 10 or items_per_page < 1:
            raise AmazonException('ValueError', 'items_per_page should be between 1 and 10')

        # Remove 10 items limit from Amazon API
        last_page_list = [False for x in range(int(item_count / items_per_page))]
        if last_page_list:
            last_page_list.pop()
        last_page_list.append(True)
        last_page_items = item_count % items_per_page

        results = []
        for last_page in last_page_list:
            if last_page and len(last_page_list) > 1:
                items_per_page = last_page_items
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
                    condition=condition,
                    currency_of_preference=currency,
                    delivery_flags=delivery,
                    item_count=items_per_page,
                    item_page=item_page,
                    keywords=keywords,
                    languages_of_preference=languages,
                    max_price=max_price,
                    merchant=merchant,
                    min_price=min_price,
                    min_reviews_rating=min_rating,
                    min_saving_percent=min_discount,
                    offer_count=1,
                    resources=SEARCH_RESOURCES,
                    search_index=search_index,
                    sort_by=sort_by,
                    title=title
                )
            except Exception as exception:
                raise AmazonException(exception.status, exception.reason)

            try:
                # Wait before doing the request
                wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                self.last_query_time = time.time()

                # Send the request and create results
                if async_req:
                    thread = self.api.search_items(request, async_req=True)
                    response = thread.get()
                else:
                    response = self.api.search_items(request)
                if response.search_result is not None:
                    for item in response.search_result.items:
                        results.append(parse_product(item))
                if response.errors is not None:
                    raise AmazonException(response.errors[0].code, response.errors[0].message)

            except Exception as exception:
                raise AmazonException(exception.reason, exception.body)
            item_page += 1

        if results:
            return results
        else:
            return None
