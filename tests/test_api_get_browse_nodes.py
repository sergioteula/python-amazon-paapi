import unittest
from unittest import mock

from amazon_paapi import AmazonApi, models
from amazon_paapi.helpers import requests


class TestGetBrowseNodes(unittest.TestCase):
    @mock.patch.object(requests, "get_browse_nodes_response")
    def test_search_items(self, mocked_get_browse_nodes_response):
        mocked_response = []
        mocked_get_browse_nodes_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_browse_nodes(['ABCDEFGHIJ'])
        self.assertTrue(isinstance(response, list))
