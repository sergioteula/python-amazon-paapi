import unittest
from operator import imod
from unittest import mock

from amazon_paapi.helpers.items import sort_items


class MockedItem(mock.MagicMock):
    def __init__(self, asin):
        super().__init__()
        self.asin = asin


class TestHelpersItems(unittest.TestCase):
    def setUp(self):
        self.mocked_items = [
            MockedItem("B"),
            MockedItem("C"),
            MockedItem("A"),
            MockedItem("D"),
        ]
        self.mocked_items_ids = ["B", "A", "D", "C", "E", "A"]

    def test_sort_items(self):
        sorted_items = sort_items(self.mocked_items, self.mocked_items_ids, False)
        self.assertEqual(sorted_items[0].asin, "B")
        self.assertEqual(sorted_items[1].asin, "A")
        self.assertEqual(sorted_items[2].asin, "D")
        self.assertEqual(sorted_items[3].asin, "C")

    def test_sort_items_include_unavailable(self):
        sorted_items = sort_items(self.mocked_items, self.mocked_items_ids, True)
        self.assertEqual(sorted_items[4].asin, "E")
        self.assertEqual(len(sorted_items), 6)

    def test_sort_items_not_include_unavailable(self):
        sorted_items = sort_items(self.mocked_items, self.mocked_items_ids, False)
        self.assertEqual(sorted_items[4].asin, "A")
        self.assertEqual(len(sorted_items), 5)

    def test_sort_items_include_repeated(self):
        sorted_items = sort_items(self.mocked_items, self.mocked_items_ids, True)
        self.assertEqual(sorted_items[1].asin, sorted_items[5].asin)
