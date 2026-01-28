"""Unit tests for tools module."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.errors import InvalidArgumentError
from amazon_creatorsapi.tools import get_asin, get_items_ids


class TestGetAsin(unittest.TestCase):
    """Tests for get_asin function."""

    def test_get_asin_with_valid_asin(self) -> None:
        """Test extracting ASIN when input is already an ASIN."""
        self.assertEqual(get_asin("B0DLFMFBJW"), "B0DLFMFBJW")

    def test_get_asin_with_lowercase_asin(self) -> None:
        """Test that lowercase ASINs are converted to uppercase."""
        self.assertEqual(get_asin("b0dlfmfbjw"), "B0DLFMFBJW")

    def test_get_asin_with_dp_url(self) -> None:
        """Test extracting ASIN from dp URL."""
        url = "https://www.amazon.com/dp/B0DLFMFBJW"
        self.assertEqual(get_asin(url), "B0DLFMFBJW")

    def test_get_asin_with_gp_product_url(self) -> None:
        """Test extracting ASIN from gp/product URL."""
        url = "https://www.amazon.com/gp/product/B01N5IB20Q"
        self.assertEqual(get_asin(url), "B01N5IB20Q")

    def test_get_asin_with_gp_aw_d_url(self) -> None:
        """Test extracting ASIN from gp/aw/d URL."""
        url = "https://www.amazon.com/gp/aw/d/B0DLFMFBJW"
        self.assertEqual(get_asin(url), "B0DLFMFBJW")

    def test_get_asin_with_dp_product_url(self) -> None:
        """Test extracting ASIN from dp/product URL."""
        url = "https://www.amazon.com/dp/product/B0DLFMFBJW"
        self.assertEqual(get_asin(url), "B0DLFMFBJW")

    def test_get_asin_with_url_with_extra_parameters(self) -> None:
        """Test extracting ASIN from URL with query parameters."""
        url = "https://www.amazon.com/dp/B0DLFMFBJW?tag=mytag&ref=pd_sl"
        self.assertEqual(get_asin(url), "B0DLFMFBJW")

    def test_get_asin_with_complex_url(self) -> None:
        """Test extracting ASIN from complex product URL with title."""
        url = "https://www.amazon.com/Product-Name-Description/dp/B0DLFMFBJW/ref=sr_1_1"
        self.assertEqual(get_asin(url), "B0DLFMFBJW")

    def test_get_asin_with_invalid_input_raises_error(self) -> None:
        """Test that invalid input raises InvalidArgumentError."""
        with self.assertRaises(InvalidArgumentError):
            get_asin("invalid_asin")

    def test_get_asin_with_too_short_string_raises_error(self) -> None:
        """Test that string shorter than 10 chars raises error."""
        with self.assertRaises(InvalidArgumentError):
            get_asin("B0DLF")

    def test_get_asin_with_too_long_string_raises_error(self) -> None:
        """Test that string longer than 10 chars raises error."""
        with self.assertRaises(InvalidArgumentError):
            get_asin("B0DLFMFBJWEXTRA")


class TestGetItemsIds(unittest.TestCase):
    """Tests for get_items_ids function."""

    def test_get_items_ids_with_single_asin_string(self) -> None:
        """Test parsing a single ASIN string."""
        self.assertEqual(get_items_ids("B0DLFMFBJW"), ["B0DLFMFBJW"])

    def test_get_items_ids_with_comma_separated_asins(self) -> None:
        """Test parsing comma-separated ASINs."""
        result = get_items_ids("B0DLFMFBJW, B01N5IB20Q")
        self.assertEqual(result, ["B0DLFMFBJW", "B01N5IB20Q"])

    def test_get_items_ids_with_list_of_asins(self) -> None:
        """Test parsing a list of ASINs."""
        result = get_items_ids(["B0DLFMFBJW", "B01N5IB20Q"])
        self.assertEqual(result, ["B0DLFMFBJW", "B01N5IB20Q"])

    def test_get_items_ids_with_list_of_urls(self) -> None:
        """Test parsing a list of Amazon URLs."""
        urls = [
            "https://www.amazon.com/dp/B0DLFMFBJW",
            "https://www.amazon.com/gp/product/B01N5IB20Q",
        ]
        result = get_items_ids(urls)
        self.assertEqual(result, ["B0DLFMFBJW", "B01N5IB20Q"])

    def test_get_items_ids_with_mixed_input(self) -> None:
        """Test parsing mixed ASINs and URLs."""
        items = ["B0DLFMFBJW", "https://www.amazon.com/dp/B01N5IB20Q"]
        result = get_items_ids(items)
        self.assertEqual(result, ["B0DLFMFBJW", "B01N5IB20Q"])

    def test_get_items_ids_strips_whitespace(self) -> None:
        """Test that whitespace is stripped from items."""
        result = get_items_ids("  B0DLFMFBJW  ,  B01N5IB20Q  ")
        self.assertEqual(result, ["B0DLFMFBJW", "B01N5IB20Q"])

    def test_get_items_ids_with_invalid_asin_raises_error(self) -> None:
        """Test that invalid ASIN in list raises error."""
        with self.assertRaises(InvalidArgumentError):
            get_items_ids(["B0DLFMFBJW", "invalid"])


if __name__ == "__main__":
    unittest.main()
