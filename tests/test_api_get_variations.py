import unittest
from unittest import mock

from amazon_paapi import AmazonApi, models
from amazon_paapi.helpers import requests


class TestGetVariations(unittest.TestCase):
    @mock.patch.object(requests, "get_variations_response")
    def test_get_variations(self, mocked_get_variations_response):
        mocked_response = models.VariationsResult()
        mocked_response.items = []
        mocked_get_variations_response.return_value = mocked_response
        amazon = AmazonApi("key", "secret", "tag", "ES")
        response = amazon.get_variations("ABCDEFGHIJ")
        self.assertTrue(isinstance(response.items, list))
