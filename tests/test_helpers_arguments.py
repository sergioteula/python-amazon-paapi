import unittest

from amazon_paapi.errors import AsinNotFoundException, InvalidArgumentException
from amazon_paapi.helpers.arguments import get_items_ids


class TestHelpersArguments(unittest.TestCase):
    def test_get_items_ids(self):
        amazon_url = "https://www.amazon.es/gp/product/B07PHPXHQS"
        self.assertEqual(get_items_ids("B01N5IB20Q"), ["B01N5IB20Q"])
        self.assertEqual(
            get_items_ids("B01N5IB20Q,B01N5IB20Q,B01N5IB20Q"),
            ["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"],
        )
        self.assertEqual(
            get_items_ids(["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"]),
            ["B01N5IB20Q", "B01N5IB20Q", "B01N5IB20Q"],
        )
        self.assertEqual(get_items_ids(amazon_url), ["B07PHPXHQS"])
        self.assertEqual(
            get_items_ids([amazon_url, amazon_url]), ["B07PHPXHQS", "B07PHPXHQS"]
        )

    def test_get_items_ids_asin_not_found(self):
        with self.assertRaises(AsinNotFoundException):
            get_items_ids("https://www.amazon.es/gp/")

    def test_get_items_ids_invalid_argument(self):
        with self.assertRaises(InvalidArgumentException):
            get_items_ids(34)
