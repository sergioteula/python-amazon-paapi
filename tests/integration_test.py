"""Integration tests for Amazon Product Advertising API."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, ClassVar, cast
from unittest import TestCase, skipUnless

from amazon_paapi.api import AmazonApi

if TYPE_CHECKING:
    from amazon_paapi.models import BrowseNode, CountryCode
    from amazon_paapi.models.item_result import Item
    from amazon_paapi.models.search_result import SearchResult
    from amazon_paapi.models.variations_result import VariationsResult


def get_api_credentials() -> tuple[str, str, str, CountryCode]:
    """Get API credentials from environment variables.

    Raises:
        ValueError: If any required credential is missing.
    """
    credentials = {
        "API_KEY": os.environ.get("API_KEY"),
        "API_SECRET": os.environ.get("API_SECRET"),
        "AFFILIATE_TAG": os.environ.get("AFFILIATE_TAG"),
        "COUNTRY_CODE": os.environ.get("COUNTRY_CODE"),
    }

    missing = [key for key, value in credentials.items() if value is None]
    if missing:
        msg = f"Missing environment variables: {', '.join(missing)}"
        raise ValueError(msg)

    return (
        cast("str", credentials["API_KEY"]),
        cast("str", credentials["API_SECRET"]),
        cast("str", credentials["AFFILIATE_TAG"]),
        cast("CountryCode", credentials["COUNTRY_CODE"]),
    )


def has_api_credentials() -> bool:
    """Check if all API credentials are available."""
    try:
        get_api_credentials()
    except ValueError:
        return False
    return True


@skipUnless(has_api_credentials(), "Needs Amazon API credentials")
class IntegrationTest(TestCase):
    """Integration tests that make real API calls to Amazon.

    All API results are cached at class level to minimize the number of
    requests. This reduces costs and avoids rate limiting.
    """

    api: ClassVar[AmazonApi]
    affiliate_tag: ClassVar[str]
    search_result: ClassVar[SearchResult]
    item_with_offers: ClassVar[Item]
    get_items_result: ClassVar[list[Item]]
    variations_result: ClassVar[VariationsResult]
    browse_nodes_result: ClassVar[list[BrowseNode]]

    @classmethod
    def setUpClass(cls) -> None:
        """Set up API client and make shared API calls once for all tests."""
        api_key, api_secret, affiliate_tag, country_code = get_api_credentials()

        cls.api = AmazonApi(api_key, api_secret, affiliate_tag, country_code)
        cls.affiliate_tag = affiliate_tag

        cls.search_result = cls.api.search_items(keywords="laptop")

        cls.item_with_offers = next(
            (item for item in cls.search_result.items if item.offers_v2 is not None),
            cls.search_result.items[0],
        )
        cls.get_items_result = cls.api.get_items(cls.item_with_offers.asin)

        item_with_variations = next(
            (item for item in cls.search_result.items if item.parent_asin),
            cls.search_result.items[0],
        )
        cls.variations_result = cls.api.get_variations(
            item_with_variations.parent_asin or item_with_variations.asin
        )

        item_with_browse_nodes = next(
            (
                item
                for item in cls.search_result.items
                if item.browse_node_info and item.browse_node_info.browse_nodes
            ),
            None,
        )
        if item_with_browse_nodes:
            browse_node_id = item_with_browse_nodes.browse_node_info.browse_nodes[0].id
            cls.browse_nodes_result = cls.api.get_browse_nodes([browse_node_id])
        else:
            cls.browse_nodes_result = []

    def test_search_items_returns_expected_count(self) -> None:
        """Test that search returns the default number of items."""
        self.assertEqual(10, len(self.search_result.items))

    def test_search_items_includes_affiliate_tag(self) -> None:
        """Test that search results include the affiliate tag in URLs."""
        searched_item = self.search_result.items[0]
        self.assertIn(self.affiliate_tag, searched_item.detail_page_url)

    def test_search_items_returns_offers_v2(self) -> None:
        """Test that search results include OffersV2 data."""
        self.assertGreater(len(self.search_result.items), 0)

        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsNotNone(listing)

    def test_get_items_returns_single_result(self) -> None:
        """Test that get_items returns exactly one item when given one ASIN."""
        self.assertEqual(1, len(self.get_items_result))

    def test_get_items_includes_affiliate_tag(self) -> None:
        """Test that get_items results include the affiliate tag in URLs."""
        self.assertIn(self.affiliate_tag, self.get_items_result[0].detail_page_url)

    def test_get_items_returns_offers_v2(self) -> None:
        """Test that get_items returns OffersV2 data."""
        item = self.get_items_result[0]
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsNotNone(listing)

    def test_get_variations_returns_items(self) -> None:
        """Test that get_variations returns a list of variation items."""
        self.assertIsNotNone(self.variations_result)
        self.assertGreater(len(self.variations_result.items), 0)

    def test_get_variations_returns_variation_summary(self) -> None:
        """Test that get_variations returns variation summary."""
        self.assertIsNotNone(self.variations_result.variation_summary)
        self.assertGreater(self.variations_result.variation_summary.variation_count, 0)

    def test_get_variations_items_include_affiliate_tag(self) -> None:
        """Test that variation items include the affiliate tag in URLs."""
        item = self.variations_result.items[0]
        self.assertIn(self.affiliate_tag, item.detail_page_url)

    def test_get_browse_nodes_returns_results(self) -> None:
        """Test that get_browse_nodes returns browse node information."""
        self.assertGreater(len(self.browse_nodes_result), 0)

    def test_get_browse_nodes_returns_node_info(self) -> None:
        """Test that browse nodes contain expected information."""
        node = self.browse_nodes_result[0]
        self.assertIsNotNone(node.id)
        self.assertIsNotNone(node.display_name)
