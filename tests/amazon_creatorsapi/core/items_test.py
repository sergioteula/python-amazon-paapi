"""Unit tests for the item utilities."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.items import (
    get_item_chunks,
    get_unique_items,
    sort_items,
)
from creatorsapi_python_sdk.models.item import Item


class TestGetUniqueItems(unittest.TestCase):
    """Tests for get_unique_items function."""

    def test_removes_duplicates_keeping_order(self) -> None:
        """Test that duplicates are removed and the order is kept."""
        result = get_unique_items(["B000000001", "B000000002", "B000000001"])
        self.assertEqual(result, ["B000000001", "B000000002"])

    def test_empty_list(self) -> None:
        """Test that an empty list is returned untouched."""
        self.assertEqual(get_unique_items([]), [])


class TestGetItemChunks(unittest.TestCase):
    """Tests for get_item_chunks function."""

    def test_single_chunk(self) -> None:
        """Test that a small list produces a single chunk."""
        item_ids = [f"B00000000{index}" for index in range(3)]
        self.assertEqual(list(get_item_chunks(item_ids)), [item_ids])

    def test_splits_over_the_limit(self) -> None:
        """Test that a list over the limit is split into several chunks."""
        item_ids = [f"B0000000{index:02d}" for index in range(23)]
        chunks = list(get_item_chunks(item_ids))
        self.assertEqual([len(chunk) for chunk in chunks], [10, 10, 3])
        self.assertEqual([item for chunk in chunks for item in chunk], item_ids)

    def test_empty_list(self) -> None:
        """Test that an empty list produces no chunks."""
        self.assertEqual(list(get_item_chunks([])), [])


class TestSortItems(unittest.TestCase):
    """Tests for sort_items function."""

    def setUp(self) -> None:
        self.item_ids = ["B000000001", "B000000002", "B000000003"]

    def test_sorts_by_requested_order(self) -> None:
        """Test that items follow the order of the requested identifiers."""
        items = [Item(asin="B000000003"), Item(asin="B000000001")]
        result = sort_items(items, self.item_ids, include_unavailable=False)
        self.assertEqual([item.asin for item in result], ["B000000001", "B000000003"])

    def test_includes_unavailable_items(self) -> None:
        """Test that missing items are added when they are requested."""
        items = [Item(asin="B000000002")]
        result = sort_items(items, self.item_ids, include_unavailable=True)
        self.assertEqual([item.asin for item in result], self.item_ids)
        self.assertIsNone(result[0].item_info)

    def test_ignores_items_without_asin(self) -> None:
        """Test that items without ASIN are not returned."""
        result = sort_items([Item()], self.item_ids, include_unavailable=False)
        self.assertEqual(result, [])
