import unittest
from unittest import mock

from amazon_paapi import AmazonApi, models
from amazon_paapi.helpers import requests


class TestGetItems(unittest.TestCase):
    @mock.patch.object(requests, "get_items_response")
    def test_get_items(self, mocked_get_items_response):
        mocked_get_items_response.return_value = []
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_items("ABCDEFGHIJ")
        self.assertTrue(isinstance(response, list))


class TestSearchItems(unittest.TestCase):
    @mock.patch.object(requests, "get_search_items_response")
    def test_search_items(self, mocked_get_search_items_response):
        mocked_response = models.SearchResult()
        mocked_response.items = []
        mocked_get_search_items_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.search_items(keywords="test")
        self.assertTrue(isinstance(response.items, list))


class TestGetVariations(unittest.TestCase):
    @mock.patch.object(requests, "get_variations_response")
    def test_get_variations(self, mocked_get_variations_response):
        mocked_response = models.VariationsResult()
        mocked_response.items = []
        mocked_get_variations_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_variations("ABCDEFGHIJ")
        self.assertTrue(isinstance(response.items, list))


class TestGetBrowseNodes(unittest.TestCase):
    @mock.patch.object(requests, "get_browse_nodes_response")
    def test_search_items(self, mocked_get_browse_nodes_response):
        mocked_response = []
        mocked_get_browse_nodes_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_browse_nodes(["ABCDEFGHIJ"])
        self.assertTrue(isinstance(response, list))
