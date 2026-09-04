"""Unit tests for the request body utilities."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.requests import get_request_body
from creatorsapi_python_sdk.models.availability import Availability
from creatorsapi_python_sdk.models.search_items_request_content import (
    SearchItemsRequestContent,
)
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource
from creatorsapi_python_sdk.models.sort_by import SortBy


class TestGetRequestBody(unittest.TestCase):
    """Tests for get_request_body function."""

    def test_uses_the_names_of_the_api(self) -> None:
        """Test that the body holds the names expected by the API."""
        request = SearchItemsRequestContent(
            partnerTag="test-tag",
            keywords="laptop",
            browseNodeId="123",
        )

        body = get_request_body(request)

        self.assertEqual(body["partnerTag"], "test-tag")
        self.assertEqual(body["browseNodeId"], "123")

    def test_drops_the_values_not_provided(self) -> None:
        """Test that the values left out are not sent to the API."""
        request = SearchItemsRequestContent(partnerTag="test-tag", keywords="laptop")

        body = get_request_body(request)

        self.assertEqual(sorted(body), ["keywords", "partnerTag"])

    def test_serializes_the_enums(self) -> None:
        """Test that enums are sent as the values of the API."""
        request = SearchItemsRequestContent(
            partnerTag="test-tag",
            keywords="laptop",
            sortBy=SortBy.PRICE_COLON_LOW_TO_HIGH,
            availability=Availability.INCLUDEOUTOFSTOCK,
            resources=[SearchItemsResource.ITEM_INFO_DOT_TITLE],
        )

        body = get_request_body(request)

        self.assertEqual(body["sortBy"], "Price:LowToHigh")
        self.assertEqual(body["availability"], "IncludeOutOfStock")
        self.assertEqual(body["resources"], ["itemInfo.title"])
