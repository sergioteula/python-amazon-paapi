"""Amazon Product Advertising API wrapper for Python

A simple Python wrapper for the last version of the Amazon Product Advertising API.
"""

import time
from typing import List, Union

from . import models
from .errors import InvalidArgumentException
from .helpers import arguments, requests
from .helpers.generators import get_list_chunks
from .helpers.items import sort_items
from .sdk.api.default_api import DefaultApi


class AmazonApi:
    """Provides methods to get information from Amazon using your API credentials.

    Args:
        key (``str``): Your API key.
        secret (``str``): Your API secret.
        tag (``str``): Your affiliate tracking id, used to create the affiliate link.
        country (``models.Country``): Country code for your affiliate account.
        throttling (``float``, optional): Wait time in seconds between API calls. Use it to avoid
            reaching Amazon limits. Defaults to 1 second.

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
            self._host = 'webservices.amazon.' + models.regions.DOMAINS[country]
            self._region = models.regions.REGIONS[country]
            self._marketplace = 'www.amazon.' + models.regions.DOMAINS[country]
        except KeyError as error:
            raise InvalidArgumentException('Country code is not correct') from error

        self._api = DefaultApi(key, secret, self._host, self._region)


    def get_items(
        self,
        items: Union[str, List[str]],
        condition: models.Condition = None,
        merchant: models.Merchant = None,
        currency_of_preference: str = None,
        languages_of_preference: List[str] = None,
        include_unavailable: bool = False,
        **kwargs
    ) -> List[models.Item]:

        """Get items information from Amazon.

        Args:
            items (``str`` | ``list[str]``): One or more items, using ASIN or product URL. Items
                in string format should be separated by commas.
            condition (``models.Condition``, optional): Filters offers by condition type.
                Defaults to Any.
            merchant (``models.Merchant``, optional): Filters search results to return items having
                at least one offer sold by target merchant. Defaults to All.
            currency_of_preference (``str``, optional): Currency of preference in which the prices
                information should be returned. Expected currency code format is ISO 4217.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            include_unavailable (``bool``, optional): The returned list includes not available
                items. Not available items have the ASIN and item_info equals None. Defaults to False.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``list[models.Item]``: A list of items with Amazon information.

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

        items_ids = arguments.get_items_ids(items)
        results = []

        for asin_chunk in get_list_chunks(list(set(items_ids)), chunk_size=10):
            request = requests.get_items_request(self, asin_chunk, **kwargs)
            self._throttle()
            items_response = requests.get_items_response(self, request)
            results.extend(items_response)

        return sort_items(results, items_ids, include_unavailable)


    def search_items(
        self,
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
        delivery_flags: List[str] = None,
        languages_of_preference: List[str] = None,
        merchant: models.Merchant = None,
        max_price: int = None,
        min_price: int = None,
        min_saving_percent: int = None,
        min_reviews_rating: int = None,
        search_index: str = None,
        sort_by: models.SortBy = None,
        **kwargs
    ) -> models.SearchResult:
        """Searches for items on Amazon based on a search query. At least one of the following
        parameters should be specified: ``keywords``, ``actor``, ``artist``, ``author``,
        ``brand``, ``title``, ``browse_node_id`` or ``search_index``.

        Args:
            item_count (``int``, optional): Number of items returned. Should be between 1 and 10.
                Defaults to 10.
            item_page (``int``, optional): The specific page of items to be returned from the available
                results. Should be between 1 and 10. Defaults to 1.
            actor (``str``, optional): Actor name associated with the item.
            artist (``str``, optional): Artist name associated with the item.
            author (``str``, optional): Author name associated with the item.
            brand (``str``, optional): Brand name associated with the item.
            keywords (``str``, optional): A word or phrase that describes an item.
            title (``str``, optional): Title associated with the item.
            availability (``models.Availability``, optional): Filters available items on Amazon.
                Defaults to Available.
            browse_node_id (``str``, optional): A unique ID assigned by Amazon that identifies a product
                category or subcategory.
            condition (``models.Condition``, optional): Filters offers by condition type. Defaults to Any.
            currency_of_preference (``str``, optional): Currency of preference in which the prices
                information should be returned. Expected currency code format is ISO 4217.
            delivery_flags (``list[str]``): Filters items which satisfy a certain delivery program.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            merchant (``models.Merchant``, optional): Filters search results to return items having
                at least one offer sold by target merchant. Defaults to All.
            max_price (``int``, optional): Filters search results to items with at least one offer price
                below the specified value. Prices appear in lowest currency denomination.
                For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.
            min_price (``int``, optional): Filters search results to items with at least one offer price
                above the specified value. Prices appear in lowest currency denomination.
                For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.
            min_saving_percent (``int``, optional): Filters search results to items with at least one
                offer having saving percentage above the specified value. Value should be
                positive integer less than 100.
            min_reviews_rating (``int``, optional): Filters search results to items with customer review
                ratings above specified value. Value should be positive integer less than 5.
            search_index (``str``, optional): Indicates the product category to search. Defaults to All.
            sort_by (``models.SortBy``, optional): The way in which items are sorted.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``models.SearchResult``: The search result containing the list of items.

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

        arguments.check_search_args(**kwargs)
        request = requests.get_search_items_request(self, **kwargs)
        self._throttle()
        return requests.get_search_items_response(self, request)


    def get_variations(
        self,
        asin: str,
        variation_count: int = None,
        variation_page: int = None,
        condition: models.Condition = None,
        currency_of_preference: str = None,
        languages_of_preference: List[str] = None,
        merchant: models.Merchant = None,
        **kwargs
    ) -> models.VariationsResult:
        """Returns a set of items that are the same product, but differ according to a
        consistent theme, for example size and color. A variation is a child ASIN.

        Args:
            asin (``str``): One item, using ASIN or product URL.
            variation_count (``int``, optional): Number of items returned. Should be between 1 and 10.
                Defaults to 10.
            variation_page (``int``, optional): The specific page of items to be returned from the available
                results. Should be between 1 and 10. Defaults to 1.
            condition (``models.Condition``, optional): Filters offers by condition type. Defaults to Any.
            currency_of_preference (``str``, optional): Currency of preference in which the prices
                information should be returned. Expected currency code format is ISO 4217.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            merchant (``models.Merchant``, optional): Filters search results to return items having
                at least one offer sold by target merchant. Defaults to All.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``models.VariationsResult``: The variations result containing the list of items.

        Raises:
            ``InvalidArgumentException``
            ``MalformedRequestException``
            ``ApiRequestException``
            ``ItemsNotFoudException``
        """

        asin = arguments.get_items_ids(asin)[0]

        kwargs.update({
            'asin': asin,
            'variation_count': variation_count,
            'variation_page': variation_page,
            'condition': condition,
            'currency_of_preference': currency_of_preference,
            'languages_of_preference': languages_of_preference,
            'merchant': merchant
        })

        arguments.check_variations_args(**kwargs)
        request = requests.get_variations_request(self, **kwargs)
        self._throttle()
        return requests.get_variations_response(self, request)


    def get_browse_nodes(
        self,
        browse_node_ids: List[str],
        languages_of_preference: List[str] = None,
        **kwargs
    ) -> List[models.BrowseNode]:
        """Returns the specified browse node's information like name, children and ancestors.

        Args:
            browse_node_ids (``list[str]``): List of browse node ids. A browse node id is a unique
                ID assigned by Amazon that identifies a product category/sub-category.
            languages_of_preference (``list[str]``, optional): Languages in order of preference in
                which the item information should be returned.
            kwargs (``dict``, optional): Any other arguments to be passed to the Amazon API.

        Returns:
            ``list[models.BrowseNode]``: A list of browse nodes.

        Raises:
            ``InvalidArgumentException``
            ``MalformedRequestException``
            ``ApiRequestException``
            ``ItemsNotFoudException``
        """

        kwargs.update({
            'browse_node_ids': browse_node_ids,
            'languages_of_preference': languages_of_preference
        })

        arguments.check_browse_nodes_args(**kwargs)
        request = requests.get_browse_nodes_request(self, **kwargs)
        self._throttle()
        return requests.get_browse_nodes_response(self, request)


    def _throttle(self):
        wait_time = self._throttling - (time.time() - self._last_query_time)
        if wait_time > 0:
            time.sleep(wait_time)
        self._last_query_time = time.time()
