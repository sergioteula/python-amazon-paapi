"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
This module allows to get product information from Amazon using the official API in
an easier way.
"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.condition import Condition
from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.partner_type import PartnerType
import time
from constant import DOMAINS, REGIONS, PRODUCT_RESOURCES
from exception import AmazonException
from parser import parse_product
from tools import get_asin, chunks


class AmazonAPI:
    """Creates an instance containing your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        tag (str): The tag you want to use for the URL.
        country (str): Country code (AU, BR, CA, FR, DE, IN, IT, JP, MX, ES, TR, AE, UK, US).
        throttling (float, optional): Reduce this value to wait longer between API calls.
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

    def get_products(self, product_ids: [str, list], condition=Condition.ANY):
        """Find product information for multiple products on Amazon.

        Args:
            product_ids (str|list): One or more item IDs like ASIN or product URL.
            Use a string separated by comma or as a list.
            condition (str, optional): Specify the product condition. Defaults to ANY.

        Returns:
            list of instances: A list containing 1 instance for each product.
        """
        api = DefaultApi(access_key=self.key,
                         secret_key=self.secret,
                         host=self.host,
                         region=self.region)

        # Clean up input data into a list stripping any extra white space
        asin_or_url_list = ([x.strip() for x in product_ids.split(",")]
                            if isinstance(product_ids, str) else product_ids)

        # Extract ASIN if supplied input is product URL and remove any duplicate ASIN
        asin_full_list = list(set([get_asin(x) for x in asin_or_url_list]))

        # Creates lists of 10 items each
        asin_full_list = list(chunks(asin_full_list, 10))

        results = []
        for asin_list in asin_full_list:
            try:
                request = GetItemsRequest(partner_tag=self.tag,
                                          partner_type=PartnerType.ASSOCIATES,
                                          marketplace=self.marketplace,
                                          condition=condition,
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

                response = api.get_items(request)
                if response.items_result is not None:
                    if len(response.items_result.items) > 0:
                        for item in response.items_result.items:
                            product = parse_product(item)
                            results.append(product)
            except Exception as exception:
                raise AmazonException(exception.status, exception.reason)

        if results:
            return results
        else:
            return None

    def get_product(self, product_id: str, condition=Condition.ANY):
        """Find product information for a specific product on Amazon.

        Args:
            product_id (str): One item ID like ASIN or product URL.
            condition (str, optional): Specify the product condition. Defaults to ANY.

        Returns:
            instance: An instance containing all the available information for the product.
        """
        if isinstance(product_id, list):
            raise AmazonException('TypeError', 'product ID should be string, not list')
        if isinstance(product_id, str):
            check_product_id = product_id.split(',')
            if len(check_product_id) > 1:
                raise AmazonException('ValueError', 'only 1 product ID is allowed, use '
                                                    'get_products for multiple requests')
        return self.get_products(product_id, condition=condition)[0]
