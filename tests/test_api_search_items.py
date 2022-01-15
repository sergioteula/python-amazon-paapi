import unittest
from unittest import mock

from amazon_paapi import AmazonApi, models
from amazon_paapi.helpers import requests


class TestSearchItems(unittest.TestCase):
    @mock.patch.object(requests, "get_search_items_response")
    def test_search_items(self, mocked_get_search_items_response):
        mocked_response = models.SearchResult()
        mocked_response.items = []
        mocked_get_search_items_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.search_items(keywords="test")
        self.assertTrue(isinstance(response.items, list))
