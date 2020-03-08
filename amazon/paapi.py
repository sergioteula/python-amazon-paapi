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

    def get_products(self, product_ids: [str, list], condition='ANY'):
        """Find product information for multiple products on Amazon.

        Args:
            product_ids (str|list): One or more item IDs like ASIN or product URL.
                Use a string separated by comma or as a list.
            condition (str, optional): Specify the product condition (ANY,
                COLLECTIBLE, NEW, REFURBISHED, USED). Defaults to ANY.

        Returns:
            list of instances: A list containing 1 instance for each product
                or None if no results.
        """

        # Clean up input data
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

    def get_product(self, product_id: str, condition='ANY'):
        """Find product information for a specific product on Amazon.

        Args:
            product_id (str): One item ID like ASIN or product URL.
            condition (str, optional): Specify the product condition (ANY,
                COLLECTIBLE, NEW, REFURBISHED, USED). Defaults to ANY.

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
        return self.get_products(product_id, condition=condition)[0]

    def search_products(self, item_count=10, item_page=1, actor=None, artist=None, author=None,
                        availability=None, brand=None, browse_node_id=None, condition=None,
                        currency_of_preference=None, delivery_flags=None, keywords=None,
                        languages_of_preference=None, max_price=None, merchant='All', min_price=None,
                        min_reviews_rating=None, min_saving_percent=None, offer_count=1,
                        search_index='All', sort_by=None, title=None,
                        async_req=False):
        try:
            if item_count > 10 or item_count < 1:
                item_count = 10

            request = SearchItemsRequest(
                partner_tag=self.tag,
                partner_type=PartnerType.ASSOCIATES,
                actor=actor,
                artist=artist,
                author=author,
                availability=availability,
                brand=brand,
                browse_node_id=browse_node_id,
                condition=condition,
                currency_of_preference=currency_of_preference,
                delivery_flags=delivery_flags,
                item_count=item_count,
                item_page=item_page,
                keywords=keywords,
                languages_of_preference=languages_of_preference,
                max_price=max_price,
                merchant=merchant,
                min_price=min_price,
                min_reviews_rating=min_reviews_rating,
                min_saving_percent=min_saving_percent,
                offer_count=offer_count,
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

            if async_req:
                thread = self.api.search_items(request, async_req=True)
                response = thread.get()
            else:
                response = self.api.search_items(request)
            if response.search_result is not None:
                resp = [parse_product(item) for item in response.search_result.items]
                return resp
            if response.errors is not None:
                raise AmazonException(response.errors[0].code, response.errors[0].message)

        except Exception as exception:
            raise AmazonException(exception.status, exception.reason)
