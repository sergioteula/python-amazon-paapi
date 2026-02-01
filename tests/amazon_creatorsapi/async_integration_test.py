"""Integration tests for AsyncAmazonCreatorsApi class."""

from __future__ import annotations

import asyncio
import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import IsolatedAsyncioTestCase, skipUnless

from dotenv import load_dotenv

from amazon_creatorsapi import AsyncAmazonCreatorsApi
from amazon_creatorsapi.errors import ItemsNotFoundError

if TYPE_CHECKING:
    from creatorsapi_python_sdk.models.browse_node import BrowseNode
    from creatorsapi_python_sdk.models.item import Item
    from creatorsapi_python_sdk.models.search_result import SearchResult
    from creatorsapi_python_sdk.models.variations_result import VariationsResult

# Load environment variables from .env file
load_dotenv(Path(__file__).parents[2] / ".env")


def get_api_credentials() -> tuple[
    str | None, str | None, str | None, str | None, str | None, str | None
]:
    """Get API credentials from environment variables.

    Returns:
        Tuple of credentials, with None for missing values.
    """
    return (
        os.environ.get("CREDENTIAL_ID"),
        os.environ.get("CREDENTIAL_SECRET"),
        os.environ.get("API_VERSION"),
        os.environ.get("AFFILIATE_TAG"),
        os.environ.get("MARKETPLACE"),
        os.environ.get("COUNTRY_CODE"),
    )


def has_api_credentials() -> bool:
    """Check if all API credentials are available."""
    (
        credential_id,
        credential_secret,
        api_version,
        affiliate_tag,
        marketplace,
        country_code,
    ) = get_api_credentials()

    # Need critical credentials
    if not all([credential_id, credential_secret, api_version, affiliate_tag]):
        return False

    # Need at least marketplace or country_code
    return bool(marketplace or country_code)


def _has_valid_offer(item: Item) -> bool:
    """Check if an item has a valid offer with price and availability."""
    if item.offers_v2 is None or not item.offers_v2.listings:
        return False

    listing = item.offers_v2.listings[0]

    has_price = (
        listing.price is not None
        and listing.price.money is not None
        and listing.price.money.amount is not None
    )

    is_available = (
        listing.availability is None
        or listing.availability.type is None
        or listing.availability.type != "OutOfStock"
    )

    return has_price and is_available


def _find_item_with_offers(items: list[Item], search_result: SearchResult) -> Item:
    """Find an item with offers, price, and in stock."""
    return next(
        (item for item in items if _has_valid_offer(item)),
        items[0] if items else search_result.items[0],  # type: ignore[index]
    )


def _find_variation_asin(items: list[Item], search_result: SearchResult) -> str | None:
    """Find ASIN to use for variations lookup."""
    item_with_variations = next(
        (item for item in items if item.parent_asin),
        None,
    )

    if item_with_variations:
        return item_with_variations.parent_asin

    if search_result.items:
        return search_result.items[0].asin

    return None


async def _run_api_setup() -> dict[str, object]:
    """Run all API calls once and return cached data."""
    (
        credential_id,
        credential_secret,
        api_version,
        affiliate_tag,
        marketplace,
        country_code,
    ) = get_api_credentials()

    api = AsyncAmazonCreatorsApi(
        credential_id=credential_id,  # type: ignore[arg-type]
        credential_secret=credential_secret,  # type: ignore[arg-type]
        version=api_version,  # type: ignore[arg-type]
        tag=affiliate_tag,  # type: ignore[arg-type]
        marketplace=marketplace,
        country=country_code,  # type: ignore[arg-type]
        throttling=1,
    )

    data: dict[str, object] = {}

    async with api:
        # 1. Search items
        search_result = await api.search_items(keywords="laptop")
        items = search_result.items or []

        # 2. Find item with offers
        item_with_offers = _find_item_with_offers(items, search_result)

        # 3. Get items by ASIN
        get_items_result: list[Item] = []
        if item_with_offers.asin:
            get_items_result = await api.get_items([item_with_offers.asin])

        # 4. Get variations
        variations_result: VariationsResult | None = None
        target_asin = _find_variation_asin(items, search_result)
        if target_asin:
            with contextlib.suppress(ItemsNotFoundError):
                variations_result = await api.get_variations(target_asin)

        # 5. Get browse nodes
        browse_nodes_result: list[BrowseNode] = []
        item_with_browse_nodes = next(
            (
                item
                for item in items
                if item.browse_node_info and item.browse_node_info.browse_nodes
            ),
            None,
        )
        if item_with_browse_nodes:
            browse_node_info = item_with_browse_nodes.browse_node_info
            if browse_node_info and browse_node_info.browse_nodes:
                browse_node_id = browse_node_info.browse_nodes[0].id
                if browse_node_id:
                    browse_nodes_result = await api.get_browse_nodes([browse_node_id])

    # Store in data dict
    data["affiliate_tag"] = affiliate_tag
    data["search_result"] = search_result
    data["item_with_offers"] = item_with_offers
    data["get_items_result"] = get_items_result
    data["variations_result"] = variations_result
    data["browse_nodes_result"] = browse_nodes_result

    return data


# Module-level cache - run setup once when module is loaded (only if credentials exist)
_cached_data: dict[str, object] = {}
if has_api_credentials():
    _cached_data = asyncio.run(_run_api_setup())


@skipUnless(has_api_credentials(), "Needs Amazon Creators API credentials")
class AsyncIntegrationTest(IsolatedAsyncioTestCase):
    """Integration tests that make real async API calls to Amazon Creators API.

    All API results are cached at module level to minimize the number of
    requests. This reduces costs and avoids rate limiting.
    """

    NO_VARIATIONS_FOUND_MSG = "No variations found"

    def setUp(self) -> None:
        """Set up that runs before each test - loads cached data."""
        self.affiliate_tag: str = _cached_data["affiliate_tag"]  # type: ignore[assignment]
        self.search_result: SearchResult = _cached_data["search_result"]  # type: ignore[assignment]
        self.item_with_offers: Item = _cached_data["item_with_offers"]  # type: ignore[assignment]
        self.get_items_result: list[Item] = _cached_data["get_items_result"]  # type: ignore[assignment]
        self.variations_result: VariationsResult | None = _cached_data[
            "variations_result"
        ]  # type: ignore[assignment]
        self.browse_nodes_result: list[BrowseNode] = _cached_data["browse_nodes_result"]  # type: ignore[assignment]

    async def test_search_items_returns_expected_count(self) -> None:
        """Test that search returns the default number of items."""
        items = self.search_result.items
        if items:
            self.assertEqual(10, len(items))

    async def test_search_items_includes_affiliate_tag(self) -> None:
        """Test that search results include the affiliate tag in URLs."""
        if self.search_result.items:
            searched_item = self.search_result.items[0]
            if searched_item.detail_page_url:
                self.assertIn(self.affiliate_tag, searched_item.detail_page_url)

    async def test_search_items_returns_offers_v2(self) -> None:
        """Test that search results include OffersV2 data."""
        items = self.search_result.items
        self.assertIsNotNone(items)
        if items:
            self.assertGreater(len(items), 0)

        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

    async def test_offers_v2_listing_has_price_info(self) -> None:
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

    async def test_offers_v2_listing_has_merchant_info(self) -> None:
        """Test that OffersV2 listings include merchant information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.merchant_info:
                self.assertIsNotNone(listing.merchant_info.name)

    async def test_offers_v2_listing_has_condition(self) -> None:
        """Test that OffersV2 listings include condition information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.condition:
                self.assertIsNotNone(listing.condition.value)

    async def test_offers_v2_listing_has_availability(self) -> None:
        """Test that OffersV2 listings include availability information."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.availability:
                self.assertIsNotNone(listing.availability.type)

    async def test_get_items_returns_single_result(self) -> None:
        """Test that get_items returns exactly one item when given one ASIN."""
        result = self.get_items_result
        self.assertEqual(1, len(result))

    async def test_get_items_includes_affiliate_tag(self) -> None:
        """Test that get_items results include the affiliate tag in URLs."""
        if self.get_items_result:
            detail_url = self.get_items_result[0].detail_page_url
            if detail_url:
                self.assertIn(self.affiliate_tag, detail_url)

    async def test_get_items_returns_offers_v2(self) -> None:
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

    async def test_get_variations_returns_items(self) -> None:
        """Test that get_variations returns a list of variation items."""
        if self.variations_result:
            self.assertIsNotNone(self.variations_result)
            items = self.variations_result.items
            self.assertIsNotNone(items)
            if items:
                self.assertGreater(len(items), 0)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    async def test_get_variations_returns_variation_summary(self) -> None:
        """Test that get_variations returns variation summary."""
        if self.variations_result:
            summary = self.variations_result.variation_summary
            self.assertIsNotNone(summary)
            if summary:
                self.assertIsNotNone(summary.variation_count)
                self.assertGreater(summary.variation_count, 0)  # type: ignore[arg-type]
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    async def test_get_variations_items_include_affiliate_tag(self) -> None:
        """Test that variation items include the affiliate tag in URLs."""
        if self.variations_result:
            items = self.variations_result.items
            if items:
                item = items[0]
                if item.detail_page_url:
                    self.assertIn(self.affiliate_tag, item.detail_page_url)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    async def test_get_browse_nodes_returns_results(self) -> None:
        """Test that get_browse_nodes returns browse node information."""
        self.assertGreater(len(self.browse_nodes_result), 0)

    async def test_get_browse_nodes_returns_node_info(self) -> None:
        """Test that browse nodes contain expected information."""
        if self.browse_nodes_result:
            node = self.browse_nodes_result[0]
            self.assertIsNotNone(node.id)
            self.assertIsNotNone(node.display_name)

    async def test_offers_v2_listing_has_is_buy_box_winner(self) -> None:
        """Test that OffersV2 listings include is_buy_box_winner attribute."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            self.assertIsInstance(listing.is_buy_box_winner, bool)

    async def test_offers_v2_listing_has_type(self) -> None:
        """Test that OffersV2 listings include offer type."""
        item = self.item_with_offers
        self.assertIsNotNone(item.offers_v2)

        if item.offers_v2 and item.offers_v2.listings:
            listing = item.offers_v2.listings[0]
            if listing.type:
                self.assertIsNotNone(listing.type)

    async def test_offers_v2_price_has_savings_when_available(self) -> None:
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

    async def test_search_items_returns_item_info(self) -> None:
        """Test that search results include item info with title."""
        if self.search_result.items:
            item = self.search_result.items[0]
            self.assertIsNotNone(item.item_info)
            if item.item_info:
                self.assertIsNotNone(item.item_info.title)
                if item.item_info.title:
                    self.assertIsNotNone(item.item_info.title.display_value)
                    title_display = item.item_info.title.display_value
                    self.assertIsNotNone(title_display)
                    self.assertIsInstance(title_display, str)
                    if title_display:
                        self.assertGreater(len(title_display), 0)

    async def test_search_items_returns_valid_asin(self) -> None:
        """Test that search results return valid ASIN format."""
        if self.search_result.items:
            item = self.search_result.items[0]
            self.assertIsNotNone(item.asin)
            if item.asin:
                self.assertEqual(len(item.asin), 10)
                self.assertTrue(item.asin.isalnum())

    async def test_search_items_returns_images(self) -> None:
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

    async def test_get_items_returns_item_info(self) -> None:
        """Test that get_items returns item info with title."""
        if self.get_items_result:
            item = self.get_items_result[0]
            self.assertIsNotNone(item.item_info)
            if item.item_info and item.item_info.title:
                self.assertIsNotNone(item.item_info.title.display_value)

    async def test_get_variations_returns_offers_v2(self) -> None:
        """Test that get_variations returns OffersV2 data for variation items."""
        if self.variations_result and self.variations_result.items:
            item_with_offers = next(
                (item for item in self.variations_result.items if item.offers_v2),
                None,
            )
            if item_with_offers and item_with_offers.offers_v2:
                self.assertIsNotNone(item_with_offers.offers_v2)
                if item_with_offers.offers_v2.listings:
                    listing = item_with_offers.offers_v2.listings[0]
                    self.assertIsNotNone(listing)
        else:
            self.skipTest(self.NO_VARIATIONS_FOUND_MSG)

    async def test_context_manager_works_correctly(self) -> None:
        """Test that async context manager works for connection pooling."""
        (
            credential_id,
            credential_secret,
            api_version,
            affiliate_tag,
            marketplace,
            country_code,
        ) = get_api_credentials()

        api = AsyncAmazonCreatorsApi(
            credential_id=credential_id,  # type: ignore[arg-type]
            credential_secret=credential_secret,  # type: ignore[arg-type]
            version=api_version,  # type: ignore[arg-type]
            tag=affiliate_tag,  # type: ignore[arg-type]
            marketplace=marketplace,
            country=country_code,  # type: ignore[arg-type]
            throttling=1,
        )

        async with api:
            # Make a simple API call inside context manager
            result = await api.search_items(keywords="book", item_count=1)
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.items)


if __name__ == "__main__":
    import unittest

    unittest.main()
