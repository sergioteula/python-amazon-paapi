import time
import unittest
from unittest import mock

from amazon_paapi import AmazonApi, models
from amazon_paapi.errors.exceptions import InvalidArgument
from amazon_paapi.helpers import requests


class TestApi(unittest.TestCase):
    def test_api_init_invalid_argument(self):
        with self.assertRaises(InvalidArgument):
            AmazonApi("key", "secret", "tag", "invalid_country")

    def test_api_throttling_disabled(self):
        throttling = 0
        amazon = AmazonApi("key", "secret", "tag", "ES", throttling)
        start = int(time.time() * 10)
        amazon._throttle()
        amazon._throttle()

        self.assertEqual(start, int(time.time() * 10))

    def test_api_throttling_sleeps(self):
        throttling = 0.1
        amazon = AmazonApi("key", "secret", "tag", "ES", throttling)
        start = int(time.time() * 10)
        amazon._throttle()
        amazon._throttle()

        self.assertTrue(start < int(time.time() * 10))

    @mock.patch.object(requests, "get_items_response")
    def test_get_items(self, mocked_get_items_response):
        mocked_get_items_response.return_value = []
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_items("ABCDEFGHIJ")
        self.assertTrue(isinstance(response, list))

    @mock.patch.object(requests, "get_search_items_response")
    def test_search_items(self, mocked_get_search_items_response):
        mocked_response = models.SearchResult()
        mocked_response.items = []
        mocked_get_search_items_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.search_items(keywords="test")
        self.assertTrue(isinstance(response.items, list))

    @mock.patch.object(requests, "get_variations_response")
    def test_get_variations(self, mocked_get_variations_response):
        mocked_response = models.VariationsResult()
        mocked_response.items = []
        mocked_get_variations_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_variations("ABCDEFGHIJ")
        self.assertTrue(isinstance(response.items, list))

    @mock.patch.object(requests, "get_browse_nodes_response")
    def test_get_browse_nodes(self, mocked_get_browse_nodes_response):
        mocked_response = []
        mocked_get_browse_nodes_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_browse_nodes(["ABCDEFGHIJ"])
        self.assertTrue(isinstance(response, list))
