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

    def test_offers_v2_listing_has_price_info(self) -> None:
        """Test that OffersV2 listings include price information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsNotNone(listing.price)

            if listing.price and listing.price.money:
                self.assertIsNotNone(listing.price.money.amount)
                self.assertIsNotNone(listing.price.money.currency)
                self.assertIsNotNone(listing.price.money.display_amount)

    def test_offers_v2_listing_has_merchant_info(self) -> None:
        """Test that OffersV2 listings include merchant information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.merchant_info:
                self.assertIsNotNone(listing.merchant_info.name)

    def test_offers_v2_listing_has_condition(self) -> None:
        """Test that OffersV2 listings include condition information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.condition:
                self.assertIsNotNone(listing.condition.value)

    def test_offers_v2_listing_has_availability(self) -> None:
        """Test that OffersV2 listings include availability information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.availability:
                self.assertIsNotNone(listing.availability.type)

    def test_get_items_returns_single_result(self) -> None:
        """Test that get_items returns exactly one item when given one ASIN."""
        self.assertEqual(1, len(self.get_items_result))

    def test_get_items_includes_affiliate_tag(self) -> None:
        """Test that get_items results include the affiliate tag in URLs."""
        self.assertIn(self.affiliate_tag, self.get_items_result[0].detail_page_url)

    def test_get_items_returns_offers_v2(self) -> None:
        """Test that get_items returns OffersV2 data with price details."""
        item = self.get_items_result[0]
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsNotNone(listing)

            if listing.price and listing.price.money:
                self.assertIsNotNone(listing.price.money.amount)
                self.assertIsNotNone(listing.price.money.display_amount)

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

    def test_offers_v2_listing_has_is_buy_box_winner(self) -> None:
        """Test that OffersV2 listings include is_buy_box_winner attribute."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsInstance(listing.is_buy_box_winner, bool)

    def test_offers_v2_listing_has_type(self) -> None:
        """Test that OffersV2 listings include offer type."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.type:
                self.assertIsNotNone(listing.type)

    def test_offers_v2_price_has_savings_when_available(self) -> None:
        """Test that OffersV2 price includes savings info when available."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.price and listing.price.savings:
                savings = listing.price.savings
                if savings.money:
                    self.assertIsNotNone(savings.money.amount)
                if savings.percentage is not None:
                    self.assertIsInstance(savings.percentage, (int, float))

    def test_search_items_returns_item_info(self) -> None:
        """Test that search results include item info with title."""
        item = self.search_result.items[0]
        self.assertIsNotNone(item.item_info)
        self.assertIsNotNone(item.item_info.title)
        self.assertIsNotNone(item.item_info.title.display_value)
        self.assertIsInstance(item.item_info.title.display_value, str)
        self.assertGreater(len(item.item_info.title.display_value), 0)

    def test_search_items_returns_valid_asin(self) -> None:
        """Test that search results return valid ASIN format."""
        item = self.search_result.items[0]
        self.assertIsNotNone(item.asin)
        self.assertEqual(len(item.asin), 10)
        self.assertTrue(item.asin.isalnum())

    def test_search_items_returns_images(self) -> None:
        """Test that search results include product images."""
        item = self.search_result.items[0]
        self.assertIsNotNone(item.images)
        if item.images.primary:
            self.assertIsNotNone(item.images.primary.large)
            if item.images.primary.large:
                self.assertIsNotNone(item.images.primary.large.url)
                self.assertTrue(item.images.primary.large.url.startswith("http"))

    def test_get_items_returns_item_info(self) -> None:
        """Test that get_items returns item info with title."""
        item = self.get_items_result[0]
        self.assertIsNotNone(item.item_info)
        self.assertIsNotNone(item.item_info.title)
        self.assertIsNotNone(item.item_info.title.display_value)

    def test_get_variations_returns_offers_v2(self) -> None:
        """Test that get_variations returns OffersV2 data for variation items."""
        item_with_offers = next(
            (item for item in self.variations_result.items if item.offers_v2),
            None,
        )
        if item_with_offers and item_with_offers.offers_v2:
            self.assertIsNotNone(item_with_offers.offers_v2)
            if item_with_offers.offers_v2.listings:
                listing = item_with_offers.offers_v2.listings[0]
                self.assertIsNotNone(listing)
