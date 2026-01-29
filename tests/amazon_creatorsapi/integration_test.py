"""Integration tests for Amazon Creators API."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, cast
from unittest import TestCase, skipUnless

from dotenv import load_dotenv

from amazon_creatorsapi import AmazonCreatorsApi
from amazon_creatorsapi.errors import ItemsNotFoundError

if TYPE_CHECKING:
    from creatorsapi_python_sdk.models.browse_node import BrowseNode
    from creatorsapi_python_sdk.models.item import Item
    from creatorsapi_python_sdk.models.search_result import SearchResult
    from creatorsapi_python_sdk.models.variations_result import VariationsResult

# Load environment variables from .env file
load_dotenv(Path(__file__).parents[2] / ".env")


def get_api_credentials() -> tuple[str, str, str, str, str, str]:
    """Get API credentials from environment variables.

    Raises:
        ValueError: If any required credential is missing.
    """
    credentials = {
        "CREDENTIAL_ID": os.environ.get("CREDENTIAL_ID"),
        "CREDENTIAL_SECRET": os.environ.get("CREDENTIAL_SECRET"),
        "API_VERSION": os.environ.get("API_VERSION"),
        "AFFILIATE_TAG": os.environ.get("AFFILIATE_TAG"),
    }

    # We need either MARKETPLACE or COUNTRY_CODE
    marketplace = os.environ.get("MARKETPLACE")
    country_code = os.environ.get("COUNTRY_CODE")

    if not marketplace and not country_code:
        msg = "Missing MARKETPLACE or COUNTRY_CODE environment variable"
        raise ValueError(msg)

    missing = [key for key, value in credentials.items() if value is None]
    if missing:
        msg = f"Missing environment variables: {', '.join(missing)}"
        raise ValueError(msg)

    return (
        cast("str", credentials["CREDENTIAL_ID"]),
        cast("str", credentials["CREDENTIAL_SECRET"]),
        cast("str", credentials["API_VERSION"]),
        cast("str", credentials["AFFILIATE_TAG"]),
        cast("str", marketplace),
        cast("str", country_code),
    )


def has_api_credentials() -> bool:
    """Check if all API credentials are available."""
    try:
        get_api_credentials()
    except ValueError:
        return False
    return True


@skipUnless(has_api_credentials(), "Needs Amazon Creators API credentials")
class IntegrationTest(TestCase):
    """Integration tests that make real API calls to Amazon creators API.

    All API results are cached at class level to minimize the number of
    requests. This reduces costs and avoids rate limiting.
    """

    api: ClassVar[AmazonCreatorsApi]
    affiliate_tag: ClassVar[str]
    search_result: ClassVar[SearchResult]
    item_with_offers: ClassVar[Item]
    get_items_result: ClassVar[list[Item]]
    variations_result: ClassVar[VariationsResult]
    browse_nodes_result: ClassVar[list[BrowseNode]]

    NO_VARIATIONS_FOUND_MSG = "No variations found"

    @classmethod
    def _find_item_with_offers(cls, items: list[Item]) -> Item:
        """Find an item with offers, price, and in stock.

        Returns an item that:
        - Has offers_v2 with listings
        - Has a valid price (price.money.amount is not None)
        - Is not out of stock (availability.type != OutOfStock)
        """
        return next(
            (item for item in items if cls._has_valid_offer(item)),
            items[0] if items else cls.search_result.items[0],  # type: ignore[index]
        )

    @classmethod
    def _has_valid_offer(cls, item: Item) -> bool:
        """Check if an item has a valid offer with price and availability.

        Args:
            item: The item to check.

        Returns:
            True if the item has a valid offer with price and is in stock.
        """
        if item.offers_v2 is None or not item.offers_v2.listings:
            return False

        listing = item.offers_v2.listings[0]

        # Check that the listing has a valid price
        has_price = (
            listing.price is not None
            and listing.price.money is not None
            and listing.price.money.amount is not None
        )

        # Check that the product is not out of stock
        is_available = (
            listing.availability is None
            or listing.availability.type is None
            or listing.availability.type != "OutOfStock"
        )

        return has_price and is_available

    @classmethod
    def _find_variation_asin(cls, items: list[Item]) -> str | None:
        """Find ASIN to use for variations lookup."""
        item_with_variations = next(
            (item for item in items if item.parent_asin),
            None,
        )

        if item_with_variations:
            return item_with_variations.parent_asin

        if cls.search_result.items:
            return cls.search_result.items[0].asin

        return None

    @classmethod
    def _setup_variations_result(cls, items: list[Item]) -> None:
        """Set up variations result if possible."""
        target_asin = cls._find_variation_asin(items)

        if target_asin:
            with contextlib.suppress(ItemsNotFoundError):
                cls.variations_result = cls.api.get_variations(target_asin)

    @classmethod
    def _setup_browse_nodes_result(cls, items: list[Item]) -> None:
        """Set up browse nodes result if possible."""
        item_with_browse_nodes = next(
            (
                item
                for item in items
                if item.browse_node_info and item.browse_node_info.browse_nodes
            ),
            None,
        )

        if not item_with_browse_nodes:
            cls.browse_nodes_result = []
            return

        browse_node_info = item_with_browse_nodes.browse_node_info
        if not browse_node_info or not browse_node_info.browse_nodes:
            cls.browse_nodes_result = []
            return

        browse_node_id = browse_node_info.browse_nodes[0].id
        if browse_node_id:
            cls.browse_nodes_result = cls.api.get_browse_nodes([browse_node_id])
        else:
            cls.browse_nodes_result = []

    @classmethod
    def setUpClass(cls) -> None:
        """Set up API client and make shared API calls once for all tests."""
        (
            credential_id,
            credential_secret,
            api_version,
            affiliate_tag,
            marketplace,
            country_code,
        ) = get_api_credentials()

        cls.api = AmazonCreatorsApi(
            credential_id=credential_id,
            credential_secret=credential_secret,
            version=api_version,
            tag=affiliate_tag,
            marketplace=marketplace,
            country=country_code,  # type: ignore[arg-type]
            throttling=1,
        )
        cls.affiliate_tag = affiliate_tag

        cls.search_result = cls.api.search_items(keywords="laptop")
        items = cls.search_result.items or []

        # Pick an item that has offers
        cls.item_with_offers = cls._find_item_with_offers(items)

        # Get items by ASIN
        if cls.item_with_offers.asin:
            cls.get_items_result = cls.api.get_items([cls.item_with_offers.asin])
        else:
            cls.get_items_result = []

        # Set up variations and browse nodes
        cls._setup_variations_result(items)
        cls._setup_browse_nodes_result(items)

    def test_search_items_returns_expected_count(self) -> None:
        """Test that search returns the default number of items."""
        # API defaults to 10
        items = self.search_result.items
        if items:
            self.assertEqual(10, len(items))

    def test_search_items_includes_affiliate_tag(self) -> None:
        """Test that search results include the affiliate tag in URLs."""
        if self.search_result.items:
            searched_item = self.search_result.items[0]
            if searched_item.detail_page_url:
                self.assertIn(self.affiliate_tag, searched_item.detail_page_url)

    def test_search_items_returns_offers_v2(self) -> None:
        """Test that search results include OffersV2 data."""
        items = self.search_result.items
        self.assertIsNotNone(items)
        if items:
            self.assertGreater(len(items), 0)

        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsNotNone(listing)

    def test_offers_v2_listing_has_price_info(self) -> None:
        """Test that OffersV2 listings include price information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
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

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.merchant_info:
                self.assertIsNotNone(listing.merchant_info.name)

    def test_offers_v2_listing_has_condition(self) -> None:
        """Test that OffersV2 listings include condition information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.condition:
                self.assertIsNotNone(listing.condition.value)

    def test_offers_v2_listing_has_availability(self) -> None:
        """Test that OffersV2 listings include availability information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]

            if listing.availability:
                self.assertIsNotNone(listing.availability.type)

    def test_get_items_returns_single_result(self) -> None:
        """Test that get_items returns exactly one item when given one ASIN."""
        result = self.get_items_result
        self.assertEqual(1, len(result))

    def test_get_items_includes_affiliate_tag(self) -> None:
        """Test that get_items results include the affiliate tag in URLs."""
        if self.get_items_result:
            detail_url = self.get_items_result[0].detail_page_url
            if detail_url:
                self.assertIn(self.affiliate_tag, detail_url)

    def test_get_items_returns_offers_v2(self) -> None:
        """Test that get_items returns OffersV2 data with price details."""
        if self.get_items_result:
            item = self.get_items_result[0]
            self.assertIsNotNone(item.offers_v2)

            if item.offers_v2 and item.offers_v2.listings:
                listing = item.offers_v2.listings[0]
                self.assertIsNotNone(listing)

                if listing.price and listing.price.money:
                    self.assertIsNotNone(listing.price.money.amount)
                    self.assertIsNotNone(listing.price.money.display_amount)

    def test_get_variations_returns_items(self) -> None:
        """Test that get_variations returns a list of variation items."""
        if hasattr(self, "variations_result") and self.variations_result:
            self.assertIsNotNone(self.variations_result)
            items = self.variations_result.items
            self.assertIsNotNone(items)
            # We already checked self.variations_result is truthy, but items could
            # be None/empty
            if items:
                self.assertGreater(len(items), 0)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    def test_get_variations_returns_variation_summary(self) -> None:
        """Test that get_variations returns variation summary."""
        if hasattr(self, "variations_result") and self.variations_result:
            summary = self.variations_result.variation_summary
            self.assertIsNotNone(summary)
            if summary:
                self.assertIsNotNone(summary.variation_count)
                # Cast to int to satisfy mypy, assertIsNotNone guarantees it's not None
                self.assertGreater(summary.variation_count, 0)  # type: ignore[arg-type]

        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    def test_get_variations_items_include_affiliate_tag(self) -> None:
        """Test that variation items include the affiliate tag in URLs."""
        if hasattr(self, "variations_result") and self.variations_result:
            items = self.variations_result.items
            if items:
                item = items[0]
                if item.detail_page_url:
                    self.assertIn(self.affiliate_tag, item.detail_page_url)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    def test_get_browse_nodes_returns_results(self) -> None:
        """Test that get_browse_nodes returns browse node information."""
        if not hasattr(self, "browse_nodes_result"):
            self.fail("browse_nodes_result not set")
        self.assertGreater(len(self.browse_nodes_result), 0)

    def test_get_browse_nodes_returns_node_info(self) -> None:
        """Test that browse nodes contain expected information."""
        if self.browse_nodes_result:
            node = self.browse_nodes_result[0]
            self.assertIsNotNone(node.id)
            self.assertIsNotNone(node.display_name)

    def test_offers_v2_listing_has_is_buy_box_winner(self) -> None:
        """Test that OffersV2 listings include is_buy_box_winner attribute."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsInstance(listing.is_buy_box_winner, bool)

    def test_offers_v2_listing_has_type(self) -> None:
        """Test that OffersV2 listings include offer type."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.type:
                self.assertIsNotNone(listing.type)

    def test_offers_v2_price_has_savings_when_available(self) -> None:
        """Test that OffersV2 price includes savings info when available."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.price and listing.price.savings:
                savings = listing.price.savings
                if savings.money:
                    self.assertIsNotNone(savings.money.amount)
                if savings.percentage is not None:
                    self.assertIsInstance(savings.percentage, (int, float))

    def test_search_items_returns_item_info(self) -> None:
        """Test that search results include item info with title."""
        if self.search_result.items:
            item = self.search_result.items[0]
            self.assertIsNotNone(item.item_info)
            if item.item_info:
                self.assertIsNotNone(item.item_info.title)
                if item.item_info.title:
                    self.assertIsNotNone(item.item_info.title.display_value)
                if item.item_info.title:
                    title_display = item.item_info.title.display_value
                    self.assertIsNotNone(title_display)
                    self.assertIsInstance(title_display, str)
                    if title_display:
                        self.assertGreater(len(title_display), 0)

    def test_search_items_returns_valid_asin(self) -> None:
        """Test that search results return valid ASIN format."""
        if self.search_result.items:
            item = self.search_result.items[0]
            self.assertIsNotNone(item.asin)
            if item.asin:
                self.assertEqual(len(item.asin), 10)
                self.assertTrue(item.asin.isalnum())

    def test_search_items_returns_images(self) -> None:
        """Test that search results include product images."""
        if self.search_result.items:
            item = self.search_result.items[0]
            self.assertIsNotNone(item.images)
            if item.images and item.images.primary:
                self.assertIsNotNone(item.images.primary.large)
                if item.images.primary.large:
                    large_url = item.images.primary.large.url
                    self.assertIsNotNone(large_url)
                    if large_url:
                        self.assertTrue(large_url.startswith("http"))

    def test_get_items_returns_item_info(self) -> None:
        """Test that get_items returns item info with title."""
        if self.get_items_result:
            item = self.get_items_result[0]
            self.assertIsNotNone(item.item_info)
            if item.item_info and item.item_info.title:
                self.assertIsNotNone(item.item_info.title.display_value)

    def test_get_variations_returns_offers_v2(self) -> None:
        """Test that get_variations returns OffersV2 data for variation items."""
        if (
            hasattr(self, "variations_result")
            and self.variations_result
            and self.variations_result.items
        ):
            item_with_offers = next(
                (item for item in self.variations_result.items if item.offers_v2),
                None,
            )
            # Not all variations might have offers, but if we found one
            if item_with_offers and item_with_offers.offers_v2:
                self.assertIsNotNone(item_with_offers.offers_v2)
                if item_with_offers.offers_v2.listings:
                    listing = item_with_offers.offers_v2.listings[0]
                    self.assertIsNotNone(listing)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)
