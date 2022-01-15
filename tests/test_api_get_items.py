import unittest
from unittest import mock

from amazon_paapi import AmazonApi
from amazon_paapi.helpers import requests


class TestGetItems(unittest.TestCase):
    @mock.patch.object(requests, "get_items_response")
    def test_get_items(self, mocked_get_items_response):
        mocked_get_items_response.return_value = []
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_items("ABCDEFGHIJ")
        self.assertTrue(isinstance(response, list))
