"""Integration tests for the sync client of the Amazon Creators API.

The suite makes every call once in setUpClass and asserts the results from
tests that never reach the network. See tests.integration_support for the
request budget and the assertions shared with the async suite.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING
from unittest import SkipTest, skipUnless

from amazon_creatorsapi import AmazonCreatorsApi
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


def build_client(credentials: Credentials) -> AmazonCreatorsApi:
    """Build the client used to collect the snapshot of the API."""
    return AmazonCreatorsApi(
        credential_id=credentials.credential_id,
        credential_secret=credentials.credential_secret,
        version=credentials.version,
        tag=credentials.tag,
        marketplace=credentials.marketplace,
        country=credentials.country,
        throttling=1,
    )


def list_feeds(api: AmazonCreatorsApi) -> list[Feed] | None:
    """Return the feeds of the account, or None when it has no access.

    Feeds belong to a program that not every account is enrolled in, so a
    rejection is reported as no feeds instead of failing the whole suite.
    """
    try:
        return api.list_feeds()
    except (AccessDeniedError, ResourceNotFoundError):
        return None


def get_feed_url(api: AmazonCreatorsApi, feeds: list[Feed] | None) -> str | None:
    """Return the download URL of the first feed, if the account has any."""
    if not feeds:
        return None

    return api.get_feed(feeds[0].feed_name, feeds[0].feed_type)


def list_reports(api: AmazonCreatorsApi) -> list[ReportMetadata] | None:
    """Return the reports of the account, or None when it has no access."""
    try:
        return api.list_reports()
    except (AccessDeniedError, ResourceNotFoundError):
        return None


def get_report_url(
    api: AmazonCreatorsApi,
    reports: list[ReportMetadata] | None,
) -> str | None:
    """Return the download URL of the first report, if the account has any."""
    if not reports:
        return None

    return api.get_report(reports[0].filename, reports[0].report_type)


def collect_snapshot(credentials: Credentials) -> ApiSnapshot:
    """Make every API call of the suite once and cache their results.

    The search is also the discovery call: the items it returns provide the
    ASINs, the parent ASIN and the browse node identifiers of the calls that
    follow, so none of them needs a request of its own.
    """
    with build_client(credentials) as api:
        search_result = api.search_items(
            keywords=SEARCH_KEYWORDS,
            item_count=SEARCH_ITEM_COUNT,
            availability=Availability.AVAILABLE,
            condition=Condition.NEW,
            sort_by=SortBy.FEATURED,
        )
        found_items = get_found_items(search_result)

        asins = pick_item_asins(found_items)
        items = api.get_items(
            build_item_ids(asins, api.marketplace),
            include_unavailable=True,
        )

        variations = None
        variation_asin = pick_variation_asin(found_items)
        if variation_asin:
            with contextlib.suppress(ItemsNotFoundError):
                variations = api.get_variations(variation_asin)

        browse_node_ids = pick_browse_node_ids(found_items)
        browse_nodes = (
            api.get_browse_nodes(browse_node_ids) if browse_node_ids else None
        )

        # Releasing the connections must not stop the client from working
        api.close()
        feeds = list_feeds(api)
        feed_url = get_feed_url(api, feeds)

        # Dropping the token must make the next call authenticate again
        api._clear_token()
        reports = list_reports(api)
        report_url = get_report_url(api, reports)

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
class IntegrationTest(IntegrationAssertions):
    """Run the shared assertions against the sync client."""

    __test__ = True

    @classmethod
    def setUpClass(cls) -> None:
        """Collect the snapshot of the API once for the whole suite."""
        credentials = load_credentials()

        if credentials is None:
            raise SkipTest(SKIP_NO_CREDENTIALS)

        cls.snapshot = collect_snapshot(credentials)
