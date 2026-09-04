"""Integration tests for the async client of the Amazon Creators API.

The suite makes every call once in setUpClass and asserts the results from
tests that never reach the network. See tests.integration_support for the
request budget and the assertions shared with the sync suite.

The async client parses the responses by hand instead of relying on the SDK,
so it is checked against the same real payloads as the sync one.
"""

from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING
from unittest import SkipTest, skipUnless

from amazon_creatorsapi.aio import AsyncAmazonCreatorsApi
from amazon_creatorsapi.errors import (
    AccessDeniedError,
    ItemsNotFoundError,
    ResourceNotFoundError,
)
from creatorsapi_python_sdk.models.availability import Availability
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.sort_by import SortBy
from tests.integration_support import (
    SEARCH_ITEM_COUNT,
    SEARCH_KEYWORDS,
    SKIP_NO_CREDENTIALS,
    ApiSnapshot,
    Credentials,
    IntegrationAssertions,
    build_item_ids,
    get_expected_item_ids,
    get_found_items,
    has_credentials,
    load_credentials,
    pick_browse_node_ids,
    pick_item_asins,
    pick_variation_asin,
)

if TYPE_CHECKING:
    from creatorsapi_python_sdk.models.feed import Feed
    from creatorsapi_python_sdk.models.report_metadata import ReportMetadata


def build_client(credentials: Credentials) -> AsyncAmazonCreatorsApi:
    """Build the client used to collect the snapshot of the API."""
    return AsyncAmazonCreatorsApi(
        credential_id=credentials.credential_id,
        credential_secret=credentials.credential_secret,
        version=credentials.version,
        tag=credentials.tag,
        marketplace=credentials.marketplace,
        country=credentials.country,
        throttling=1,
    )


async def list_feeds(api: AsyncAmazonCreatorsApi) -> list[Feed] | None:
    """Return the feeds of the account, or None when it has no access.

    Feeds belong to a program that not every account is enrolled in, so a
    rejection is reported as no feeds instead of failing the whole suite.
    """
    try:
        return await api.list_feeds()
    except (AccessDeniedError, ResourceNotFoundError):
        return None


async def get_feed_url(
    api: AsyncAmazonCreatorsApi,
    feeds: list[Feed] | None,
) -> str | None:
    """Return the download URL of the first feed, if the account has any."""
    if not feeds:
        return None

    return await api.get_feed(feeds[0].feed_name, feeds[0].feed_type)


async def list_reports(api: AsyncAmazonCreatorsApi) -> list[ReportMetadata] | None:
    """Return the reports of the account, or None when it has no access."""
    try:
        return await api.list_reports()
    except (AccessDeniedError, ResourceNotFoundError):
        return None


async def get_report_url(
    api: AsyncAmazonCreatorsApi,
    reports: list[ReportMetadata] | None,
) -> str | None:
    """Return the download URL of the first report, if the account has any."""
    if not reports:
        return None

    return await api.get_report(reports[0].filename, reports[0].report_type)


async def collect_snapshot(credentials: Credentials) -> ApiSnapshot:
    """Make every API call of the suite once and cache their results.

    The catalog calls run inside the context manager, which keeps a pool of
    connections open, and the ones for feeds and reports run outside of it,
    where the client opens a connection for every request. Both modes are
    covered without spending a request on either of them.
    """
    api = build_client(credentials)

    async with api:
        search_result = await api.search_items(
            keywords=SEARCH_KEYWORDS,
            item_count=SEARCH_ITEM_COUNT,
            availability=Availability.AVAILABLE,
            condition=Condition.NEW,
            sort_by=SortBy.FEATURED,
        )
        found_items = get_found_items(search_result)

        asins = pick_item_asins(found_items)
        items = await api.get_items(
            build_item_ids(asins, api.marketplace),
            include_unavailable=True,
        )

        variations = None
        variation_asin = pick_variation_asin(found_items)
        if variation_asin:
            with contextlib.suppress(ItemsNotFoundError):
                variations = await api.get_variations(variation_asin)

        browse_node_ids = pick_browse_node_ids(found_items)
        browse_nodes = (
            await api.get_browse_nodes(browse_node_ids) if browse_node_ids else None
        )

    feeds = await list_feeds(api)
    feed_url = await get_feed_url(api, feeds)

    # Dropping the token must make the next call authenticate again
    api._token_manager.clear_token()
    reports = await list_reports(api)
    report_url = await get_report_url(api, reports)

    return ApiSnapshot(
        tag=credentials.tag,
        search_result=search_result,
        requested_ids=get_expected_item_ids(asins),
        items=items,
        variations=variations,
        browse_node_ids=browse_node_ids,
        browse_nodes=browse_nodes,
        feeds=feeds,
        feed_url=feed_url,
        reports=reports,
        report_url=report_url,
    )


@skipUnless(has_credentials(), SKIP_NO_CREDENTIALS)
class AsyncIntegrationTest(IntegrationAssertions):
    """Run the shared assertions against the async client."""

    __test__ = True

    @classmethod
    def setUpClass(cls) -> None:
        """Collect the snapshot of the API once for the whole suite."""
        credentials = load_credentials()

        if credentials is None:
            raise SkipTest(SKIP_NO_CREDENTIALS)

        cls.snapshot = asyncio.run(collect_snapshot(credentials))
