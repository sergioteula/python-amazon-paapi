"""Shared pieces for the integration tests that hit the real Creators API.

The account running these tests has a limited amount of requests per day, so
every call is made once, cached in an ApiSnapshot and then asserted from as
many angles as possible. Both the sync and the async suites reuse the
assertions defined here, which holds the two clients to the same contract.

Request budget per client, all of them made while building the snapshot:

    1. search_items       also the discovery call for the ones below
    2. get_items          mixes a URL, a duplicate and a missing ASIN
    3. get_variations     only when the search found an item with variations
    4. get_browse_nodes   only when the search found browse nodes
    5. list_feeds         skipped for credentials without the feeds program
    6. get_feed           only when the account has feeds
    7. list_reports       skipped for credentials without reports
    8. get_report         only when the account has reports

Nothing else reaches the network: the tests only read the snapshot, and the
extra behaviours worth checking, such as releasing the connections or getting
a new token, are folded into the calls above instead of costing a request.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, cast
from unittest import SkipTest, TestCase

from dotenv import load_dotenv

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode
    from amazon_creatorsapi.core.results import ResultList
    from creatorsapi_python_sdk.models.browse_node import BrowseNode
    from creatorsapi_python_sdk.models.feed import Feed
    from creatorsapi_python_sdk.models.item import Item
    from creatorsapi_python_sdk.models.offer_listing_v2 import OfferListingV2
    from creatorsapi_python_sdk.models.report_metadata import ReportMetadata
    from creatorsapi_python_sdk.models.search_result import SearchResult
    from creatorsapi_python_sdk.models.variations_result import VariationsResult

load_dotenv(Path(__file__).parents[1] / ".env")

# Keyword broad enough to return offers, variations and browse nodes in any
# marketplace, as the country of the credentials is not known beforehand
SEARCH_KEYWORDS = "laptop"
SEARCH_ITEM_COUNT = 10
MAX_BROWSE_NODES = 2
MAX_ITEM_ASINS = 2
ASIN_LENGTH = 10

# Well formed identifier that Amazon does not know, used to check the partial
# errors and the placeholders of a request for several items
MISSING_ASIN = "0000000000"

SKIP_NO_CREDENTIALS = "Needs Amazon Creators API credentials"
SKIP_NO_SNAPSHOT = "The suite collected no snapshot of the API"
SKIP_NO_VARIATIONS = "The search returned no item with variations"
SKIP_NO_BROWSE_NODES = "The search returned no browse nodes"
SKIP_NO_FEEDS = "The credentials have no feeds available"
SKIP_NO_REPORTS = "The credentials have no reports available"


@dataclass(frozen=True)
class Credentials:
    """Credentials and marketplace taken from the environment."""

    credential_id: str
    credential_secret: str
    version: str
    tag: str
    marketplace: str | None
    country: CountryCode | None


@dataclass(frozen=True)
class ApiSnapshot:
    """Every result of the API calls made by a suite, cached for its tests.

    A field set to None means the call was not made, either because the
    discovery call gave nothing to ask for or because the credentials cannot
    reach that part of the API. The tests reading it skip instead of failing.
    """

    tag: str
    search_result: SearchResult
    requested_ids: list[str]
    items: ResultList[Item]
    variations: VariationsResult | None
    browse_node_ids: list[str]
    browse_nodes: ResultList[BrowseNode] | None
    feeds: list[Feed] | None
    feed_url: str | None
    reports: list[ReportMetadata] | None
    report_url: str | None


def load_credentials() -> Credentials | None:
    """Read the credentials of the API from the environment.

    Returns:
        The credentials, or None when any of them is missing. A marketplace
        or a country is enough, as the client derives one from the other.

    """
    credential_id = os.environ.get("CREDENTIAL_ID")
    credential_secret = os.environ.get("CREDENTIAL_SECRET")
    version = os.environ.get("API_VERSION")
    tag = os.environ.get("AFFILIATE_TAG")
    marketplace = os.environ.get("MARKETPLACE")
    country = os.environ.get("COUNTRY_CODE")

    if not (credential_id and credential_secret and version and tag):
        return None

    if not marketplace and not country:
        return None

    return Credentials(
        credential_id=credential_id,
        credential_secret=credential_secret,
        version=version,
        tag=tag,
        marketplace=marketplace or None,
        country=cast("CountryCode", country) if country else None,
    )


def has_credentials() -> bool:
    """Tell whether the environment holds every credential the tests need."""
    return load_credentials() is not None


def get_found_items(search_result: SearchResult) -> list[Item]:
    """Return the items of a search result, empty when it carried none."""
    return list(search_result.items or [])


def has_usable_offer(item: Item) -> bool:
    """Tell whether an item is in stock and carries a price in its offer."""
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


def pick_item_asins(items: list[Item], limit: int = MAX_ITEM_ASINS) -> list[str]:
    """Return the ASINs to ask get_items for, preferring items with offers.

    Args:
        items: Items returned by the search call.
        limit: Amount of ASINs to return at most.

    Returns:
        Up to limit ASINs, the ones of items with a usable offer first, so
        the offers of the response can be asserted.

    """
    with_offers = [item for item in items if has_usable_offer(item)]
    without_offers = [item for item in items if not has_usable_offer(item)]

    return [item.asin for item in [*with_offers, *without_offers] if item.asin][:limit]


def pick_variation_asin(items: list[Item]) -> str | None:
    """Return the parent ASIN of the first item that belongs to a family."""
    return next((item.parent_asin for item in items if item.parent_asin), None)


def pick_browse_node_ids(items: list[Item], limit: int = MAX_BROWSE_NODES) -> list[str]:
    """Return distinct browse node identifiers found in the search results.

    Args:
        items: Items returned by the search call.
        limit: Amount of identifiers to return at most.

    Returns:
        Up to limit browse node identifiers, without duplicates, so a single
        call can check that every requested node comes back.

    """
    node_ids: list[str] = []

    for item in items:
        info = item.browse_node_info
        for node in (info.browse_nodes or []) if info else []:
            if node.id and node.id not in node_ids:
                node_ids.append(node.id)

    return node_ids[:limit]


def build_item_ids(asins: list[str], marketplace: str) -> list[str]:
    """Build the identifiers of the single get_items call of a suite.

    The list mixes an Amazon URL, the plain ASINs of the other items, a
    duplicate of the first one and an identifier Amazon does not know, so one
    request checks the parsing of URLs, the removal of duplicates, the order
    of the response, its partial errors and the placeholders added for the
    items that Amazon did not return.

    Args:
        asins: ASINs discovered by the search call.
        marketplace: Marketplace of the client, used to build the URL.

    Returns:
        The identifiers to request, with the duplicate still in place.

    Raises:
        RuntimeError: If the search returned no ASIN to request.

    """
    if not asins:
        msg = "The search returned no item to request by ASIN"
        raise RuntimeError(msg)

    return [
        f"https://{marketplace}/dp/{asins[0]}",
        *asins[1:],
        asins[0],
        MISSING_ASIN,
    ]


def get_expected_item_ids(asins: list[str]) -> list[str]:
    """Return the ASINs that a get_items call should answer with, in order."""
    return [*asins, MISSING_ASIN]


class IntegrationAssertions(TestCase):
    """Assertions run against the snapshot collected by each client.

    The suites of both clients inherit from this class, so the sync and the
    async implementations are held to the same contract. It is not collected
    on its own, as it has no snapshot to assert.
    """

    __test__ = False

    snapshot: ClassVar[ApiSnapshot]

    @classmethod
    def setUpClass(cls) -> None:
        """Skip the class when the suite collected no snapshot."""
        if not hasattr(cls, "snapshot"):
            raise SkipTest(SKIP_NO_SNAPSHOT)

    def test_search_returns_items_within_the_requested_count(self) -> None:
        """Test that the search honours the requested amount of items."""
        items = get_found_items(self.snapshot.search_result)
        self.assertGreater(len(items), 0)
        self.assertLessEqual(len(items), SEARCH_ITEM_COUNT)

    def test_search_returns_the_total_amount_of_results(self) -> None:
        """Test that the search reports how many results Amazon has."""
        total = self.snapshot.search_result.total_result_count

        if total is None:
            self.skipTest("The marketplace reported no total result count")

        self.assertGreater(total, 0)

    def test_search_returns_the_url_of_the_results(self) -> None:
        """Test that the search returns the URL of its results page."""
        search_url = self.snapshot.search_result.search_url

        if search_url is None:
            self.skipTest("The marketplace reported no search URL")

        self.assertTrue(search_url.startswith("http"))

    def test_search_items_have_a_valid_asin(self) -> None:
        """Test that every item of the search carries a well formed ASIN."""
        for item in get_found_items(self.snapshot.search_result):
            self.assertIsNotNone(item.asin)
            self.assertEqual(ASIN_LENGTH, len(item.asin or ""))
            self.assertTrue((item.asin or "").isalnum())

    def test_search_items_include_the_affiliate_tag(self) -> None:
        """Test that every detail page URL of the search carries the tag."""
        urls = [
            item.detail_page_url
            for item in get_found_items(self.snapshot.search_result)
            if item.detail_page_url
        ]

        self.assertGreater(len(urls), 0)
        for url in urls:
            self.assertIn(self.snapshot.tag, url)

    def test_search_items_include_a_title(self) -> None:
        """Test that the items of the search carry a non empty title."""
        titles = [
            item.item_info.title.display_value
            for item in get_found_items(self.snapshot.search_result)
            if item.item_info and item.item_info.title
        ]

        self.assertGreater(len(titles), 0)
        for title in titles:
            self.assertIsNotNone(title)
            self.assertGreater(len(title or ""), 0)

    def test_search_items_include_images(self) -> None:
        """Test that the items of the search carry the URL of their image."""
        images = [
            item.images.primary.large
            for item in get_found_items(self.snapshot.search_result)
            if item.images and item.images.primary and item.images.primary.large
        ]

        self.assertGreater(len(images), 0)
        for image in images:
            self.assertIsNotNone(image.url)
            self.assertTrue((image.url or "").startswith("http"))

    def test_search_items_include_their_browse_nodes(self) -> None:
        """Test that the items of the search carry identified browse nodes."""
        if not self.snapshot.browse_node_ids:
            self.skipTest(SKIP_NO_BROWSE_NODES)

        for node_id in self.snapshot.browse_node_ids:
            self.assertGreater(len(node_id), 0)

    def test_search_returns_an_item_with_a_usable_offer(self) -> None:
        """Test that the search returns offers with a price and stock."""
        items = get_found_items(self.snapshot.search_result)
        self.assertTrue(any(has_usable_offer(item) for item in items))

    def test_offers_include_a_complete_price(self) -> None:
        """Test that the listings of an offer carry amount and currency."""
        listing = self._get_listing_with_offer()
        price = listing.price

        if price is None or price.money is None:
            self.fail("The listing of the offer carried no price")

        self.assertIsNotNone(price.money.amount)
        self.assertIsNotNone(price.money.currency)
        self.assertIsNotNone(price.money.display_amount)

    def test_offers_describe_how_the_item_is_sold(self) -> None:
        """Test that the listings of an offer describe condition and stock."""
        listing = self._get_listing_with_offer()

        self.assertIsNotNone(listing.condition)
        self.assertIsNotNone(listing.availability)
        self.assertIsInstance(listing.is_buy_box_winner, bool)

        if listing.condition:
            self.assertIsNotNone(listing.condition.value)
        if listing.availability:
            self.assertIsNotNone(listing.availability.type)
        if listing.merchant_info:
            self.assertIsNotNone(listing.merchant_info.name)

    def test_offers_savings_are_consistent_when_present(self) -> None:
        """Test that the savings of an offer come with amount and percentage."""
        listing = self._get_listing_with_offer()
        savings = listing.price.savings if listing.price else None

        if savings is None:
            self.skipTest("The offer carried no savings")

        if savings.money:
            self.assertIsNotNone(savings.money.amount)
        if savings.percentage is not None:
            self.assertGreater(savings.percentage, 0)

    def test_get_items_returns_the_requested_ids_in_order(self) -> None:
        """Test the parsing of URLs, the deduplication and the ordering.

        A single request asks for a URL, the ASIN it points to, a duplicate of
        it and an identifier Amazon does not know, so its answer proves that
        the client parses URLs, drops duplicates and keeps the asked order.
        """
        self.assertEqual(
            self.snapshot.requested_ids,
            [item.asin for item in self.snapshot.items],
        )

    def test_get_items_reports_the_errors_of_the_missing_item(self) -> None:
        """Test that the partial errors of Amazon reach the caller."""
        errors = self.snapshot.items.errors

        self.assertGreater(len(errors), 0)
        for error in errors:
            self.assertGreater(len(error.code), 0)
            self.assertGreater(len(error.message), 0)

    def test_get_items_adds_a_placeholder_for_the_missing_item(self) -> None:
        """Test that include_unavailable adds an item with only its ASIN."""
        placeholder = self.snapshot.items[-1]

        self.assertEqual(MISSING_ASIN, placeholder.asin)
        self.assertIsNone(placeholder.item_info)
        self.assertIsNone(placeholder.detail_page_url)

    def test_get_items_returns_complete_items(self) -> None:
        """Test that the found items carry their info, URL and offers."""
        found = self.snapshot.items[:-1]
        self.assertGreater(len(found), 0)

        for item in found:
            self.assertIsNotNone(item.item_info)
            self.assertIsNotNone(item.detail_page_url)
            self.assertIn(self.snapshot.tag, item.detail_page_url or "")

        self.assertTrue(any(item.offers_v2 for item in found))

    def test_get_variations_returns_items_of_the_same_family(self) -> None:
        """Test that the variations of a product come with their attributes."""
        items = self._get_variations().items or []
        self.assertGreater(len(items), 0)

        for item in items:
            self.assertIsNotNone(item.asin)
            if item.detail_page_url:
                self.assertIn(self.snapshot.tag, item.detail_page_url)

        self.assertTrue(any(item.variation_attributes for item in items))

    def test_get_variations_returns_a_summary(self) -> None:
        """Test that the variations come with a summary counting them."""
        summary = self._get_variations().variation_summary

        if summary is None:
            self.fail("The variations came with no summary")

        if summary.variation_count is None:
            self.skipTest("The marketplace reported no variation count")

        self.assertGreater(summary.variation_count, 0)

    def test_get_browse_nodes_returns_every_requested_node(self) -> None:
        """Test that a request for several nodes answers with all of them."""
        nodes = self._get_browse_nodes()

        self.assertEqual(
            set(self.snapshot.browse_node_ids),
            {node.id for node in nodes},
        )

    def test_get_browse_nodes_returns_named_nodes(self) -> None:
        """Test that the browse nodes carry the names Amazon displays."""
        for node in self._get_browse_nodes():
            self.assertIsNotNone(node.display_name)
            self.assertIsNotNone(node.context_free_name)
            self.assertIsInstance(node.is_root, bool)

    def test_get_browse_nodes_returns_the_tree_of_a_node(self) -> None:
        """Test that the browse nodes carry their ancestors or children."""
        nodes = self._get_browse_nodes()
        self.assertTrue(any(node.ancestor or node.children for node in nodes))

    def test_list_feeds_returns_described_feeds(self) -> None:
        """Test that the feeds of the account come fully described."""
        for feed in self._get_feeds():
            self.assertGreater(len(feed.feed_name), 0)
            self.assertGreater(len(feed.md5), 0)
            self.assertGreater(len(feed.last_updated), 0)
            self.assertGreater(feed.size, 0)

    def test_get_feed_returns_a_download_url(self) -> None:
        """Test that a feed of the account can be turned into a URL."""
        self._get_feeds()
        feed_url = self.snapshot.feed_url

        self.assertIsNotNone(feed_url)
        self.assertTrue((feed_url or "").startswith("https://"))

    def test_list_reports_returns_described_reports(self) -> None:
        """Test that the reports of the account come fully described."""
        for report in self._get_reports():
            self.assertGreater(len(report.filename), 0)
            self.assertGreater(len(report.md5), 0)
            self.assertGreater(len(report.last_modified), 0)
            self.assertGreater(report.size, 0)

    def test_get_report_returns_a_download_url(self) -> None:
        """Test that a report of the account can be turned into a URL."""
        self._get_reports()
        report_url = self.snapshot.report_url

        self.assertIsNotNone(report_url)
        self.assertTrue((report_url or "").startswith("https://"))

    def _get_listing_with_offer(self) -> OfferListingV2:
        """Return the first listing of the search that has a usable offer."""
        items = get_found_items(self.snapshot.search_result)
        item = next((item for item in items if has_usable_offer(item)), None)

        if item is None or item.offers_v2 is None or not item.offers_v2.listings:
            self.skipTest("The search returned no item with a usable offer")

        return item.offers_v2.listings[0]

    def _get_variations(self) -> VariationsResult:
        """Return the cached variations, skipping the test without them."""
        if self.snapshot.variations is None:
            self.skipTest(SKIP_NO_VARIATIONS)

        return self.snapshot.variations

    def _get_browse_nodes(self) -> ResultList[BrowseNode]:
        """Return the cached browse nodes, skipping the test without them."""
        if self.snapshot.browse_nodes is None:
            self.skipTest(SKIP_NO_BROWSE_NODES)

        return self.snapshot.browse_nodes

    def _get_feeds(self) -> list[Feed]:
        """Return the cached feeds, skipping the test without them."""
        if not self.snapshot.feeds:
            self.skipTest(SKIP_NO_FEEDS)

        return self.snapshot.feeds

    def _get_reports(self) -> list[ReportMetadata]:
        """Return the cached reports, skipping the test without them."""
        if not self.snapshot.reports:
            self.skipTest(SKIP_NO_REPORTS)

        return self.snapshot.reports
