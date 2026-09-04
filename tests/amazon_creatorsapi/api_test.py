"""Unit tests for AmazonCreatorsApi class."""

from __future__ import annotations

import time
import unittest
from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import MagicMock

import urllib3

from amazon_creatorsapi import AmazonCreatorsApi
from amazon_creatorsapi.core.auth import TimeoutOAuth2TokenManager
from amazon_creatorsapi.core.constants import DEFAULT_TIMEOUT
from amazon_creatorsapi.core.oauth import VERSION_ENDPOINTS
from amazon_creatorsapi.errors import (
    AccessDeniedError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
)
from creatorsapi_python_sdk.exceptions import ApiException
from creatorsapi_python_sdk.models.availability import Availability
from creatorsapi_python_sdk.models.browse_node import BrowseNode
from creatorsapi_python_sdk.models.browse_nodes_result import BrowseNodesResult
from creatorsapi_python_sdk.models.delivery_flag import DeliveryFlag
from creatorsapi_python_sdk.models.error_data import ErrorData
from creatorsapi_python_sdk.models.feed_type import FeedType
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_browse_nodes_response_content import (
    GetBrowseNodesResponseContent,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_items_response_content import (
    GetItemsResponseContent,
)
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.item import Item
from creatorsapi_python_sdk.models.items_result import ItemsResult
from creatorsapi_python_sdk.models.report_type import ReportType
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode


class TestAmazonCreatorsApi(unittest.TestCase):
    """Tests for AmazonCreatorsApi class."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"
        self.version = "2.2"
        self.tag = "test-tag"
        self.country: CountryCode = "ES"

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_with_country(self, mock_client: MagicMock) -> None:
        """Test initialization with country code."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
        )
        self.assertEqual(api.marketplace, "www.amazon.es")
        self.assertEqual(api.tag, self.tag)
        mock_client.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_with_marketplace(self, _mock_client: MagicMock) -> None:
        """Test initialization with direct marketplace URL."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            marketplace="www.amazon.co.uk",
        )
        self.assertEqual(api.marketplace, "www.amazon.co.uk")

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_marketplace_overrides_country(self, _mock_client: MagicMock) -> None:
        """Test that marketplace parameter overrides country."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country="ES",
            marketplace="www.amazon.com",
        )
        self.assertEqual(api.marketplace, "www.amazon.com")

    def test_init_invalid_country(self) -> None:
        """Test initialization with invalid country code raises exception."""
        with self.assertRaises(InvalidArgumentError):
            AmazonCreatorsApi(
                credential_id=self.credential_id,
                credential_secret=self.credential_secret,
                version=self.version,
                tag=self.tag,
                country="INVALID",  # type: ignore[arg-type]
            )

    def test_init_no_country_or_marketplace(self) -> None:
        """Test initialization without country or marketplace raises exception."""
        with self.assertRaises(InvalidArgumentError):
            AmazonCreatorsApi(
                credential_id=self.credential_id,
                credential_secret=self.credential_secret,
                version=self.version,
                tag=self.tag,
            )

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_throttling_disabled(self, _mock_client: MagicMock) -> None:
        """Test that API call is not delayed when throttling is 0."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        start_time = time.time()
        api._throttle()
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 0.1)

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_throttling_sleeps(self, _mock_client: MagicMock) -> None:
        """Test that API call is delayed according to throttling setting."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0.2,
        )
        api._last_query_time = time.monotonic()
        start_time = time.time()
        api._throttle()
        elapsed_time = time.time() - start_time
        self.assertGreater(elapsed_time, 0.1)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items method returns items."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock(asin="B0DLFMFBJW")]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_items(["B0DLFMFBJW"])
        self.assertIsInstance(result, list)
        mock_api.get_items.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items method returns results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = MagicMock()
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.search_items(keywords="laptop")
        self.assertIsNotNone(result)
        mock_api.search_items.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_with_delivery_flags(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items forwards delivery flags to the SDK request."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = MagicMock()
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )

        result = api.search_items(
            keywords="laptop",
            delivery_flags=[DeliveryFlag.PRIME, DeliveryFlag.FREESHIPPING],
        )

        self.assertIsNotNone(result)
        request = mock_api.search_items.call_args.kwargs["search_items_request_content"]
        self.assertEqual(
            request.delivery_flags,
            [DeliveryFlag.PRIME, DeliveryFlag.FREESHIPPING],
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_no_results(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items raises ItemsNotFoundError when no items found."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result = None
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_items_none(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items raises ItemsNotFoundError when items is None."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = None
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items handles API exception."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(status=500, reason="Server Error")

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_no_results(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items raises ItemsNotFoundError when no results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = None
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.search_items(keywords="nonexistent")

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items handles API exception."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.search_items.side_effect = ApiException(
            status=500, reason="Server Error"
        )

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.search_items(keywords="laptop")

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_variations(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_variations method returns results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.variations_result = MagicMock()
        mock_api.get_variations.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_variations("B0DLFMFBJW")
        self.assertIsNotNone(result)
        mock_api.get_variations.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_variations_no_results(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_variations raises ItemsNotFoundError when no results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.variations_result = None
        mock_api.get_variations.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_variations("B0DLFMFBJW")

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_variations_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_variations handles API exception."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_variations.side_effect = ApiException(
            status=500, reason="Server Error"
        )

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_variations("B0DLFMFBJW")

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes method returns results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.browse_nodes_result.browse_nodes = [MagicMock()]
        mock_api.get_browse_nodes.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_browse_nodes(["123456"])
        self.assertIsInstance(result, list)
        mock_api.get_browse_nodes.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_no_results(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes raises ItemsNotFoundError when no results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.browse_nodes_result = None
        mock_api.get_browse_nodes.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_browse_nodes(["123456"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_browse_nodes_none(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes raises ItemsNotFoundError when browse_nodes is None."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.browse_nodes_result.browse_nodes = None
        mock_api.get_browse_nodes.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_browse_nodes(["123456"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes handles API exception."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_browse_nodes.side_effect = ApiException(
            status=500, reason="Server Error"
        )

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_browse_nodes(["123456"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_not_found(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test _handle_api_exception raises ItemsNotFoundError on 404."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(status=404, reason="Not Found")

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(ItemsNotFoundError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_too_many_requests(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test _handle_api_exception raises TooManyRequestsError on 429."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(
            status=429, reason="Too Many Requests"
        )

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(TooManyRequestsError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_invalid_parameter_value(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test raises InvalidArgumentError on InvalidParameterValue."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=400, reason="Bad Request")
        error.body = '{"errors": [{"code": "InvalidParameterValue"}]}'
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(InvalidArgumentError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_invalid_partner_tag(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test raises InvalidArgumentError on InvalidPartnerTag."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=400, reason="Bad Request")
        error.body = '{"errors": [{"code": "InvalidPartnerTag"}]}'
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(InvalidArgumentError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_invalid_associate(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test raises AssociateValidationError on InvalidAssociate."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=400, reason="Bad Request")
        error.body = '{"errors": [{"code": "InvalidAssociate"}]}'
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(AssociateValidationError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_generic_error(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test _handle_api_exception raises RequestError on generic error."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=500, reason="Internal Server Error")
        error.body = '{"message": "Something went wrong"}'
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_no_body(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test _handle_api_exception handles error with no body."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=500, reason="Internal Server Error")
        error.body = None
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_handle_api_exception_no_reason(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test _handle_api_exception handles error with no reason."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        error = ApiException(status=500)
        error.reason = None
        error.body = None
        mock_api.get_items.side_effect = error

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        with self.assertRaises(RequestError):
            api.get_items(["B0DLFMFBJW"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_with_explicit_resources(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items with explicit resources parameter."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock(asin="B0DLFMFBJW")]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_items(
            ["B0DLFMFBJW"],
            resources=[GetItemsResource.ITEM_INFO_DOT_TITLE],
        )
        self.assertIsInstance(result, list)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_with_explicit_resources(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items with explicit resources parameter."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = MagicMock()
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.search_items(
            keywords="laptop",
            resources=[SearchItemsResource.ITEM_INFO_DOT_TITLE],
        )
        self.assertIsNotNone(result)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_variations_with_explicit_resources(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_variations with explicit resources parameter."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.variations_result = MagicMock()
        mock_api.get_variations.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_variations(
            "B0DLFMFBJW",
            resources=[GetVariationsResource.ITEM_INFO_DOT_TITLE],
        )
        self.assertIsNotNone(result)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_with_explicit_resources(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes with explicit resources parameter."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.browse_nodes_result.browse_nodes = [MagicMock()]
        mock_api.get_browse_nodes.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        result = api.get_browse_nodes(
            ["123456"],
            resources=[GetBrowseNodesResource.BROWSE_NODES_DOT_ANCESTOR],
        )
        self.assertIsInstance(result, list)

    def _build_api(self) -> AmazonCreatorsApi:
        """Build an API instance with throttling disabled."""
        return AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_list_feeds(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test list_feeds method returns the available feeds."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        feed = MagicMock()
        mock_api.list_feeds.return_value = MagicMock(feeds=[feed])

        result = self._build_api().list_feeds()

        self.assertEqual([feed], result)
        mock_api.list_feeds.assert_called_once_with(
            x_marketplace="www.amazon.es",
            _request_timeout=DEFAULT_TIMEOUT,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_list_feeds_without_feeds(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test list_feeds returns an empty list when no feeds are available."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.list_feeds.return_value = MagicMock(feeds=None)

        self.assertEqual([], self._build_api().list_feeds())

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_list_feeds_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test list_feeds raises a wrapped error on API failure."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.list_feeds.side_effect = ApiException(status=500)

        with self.assertRaises(RequestError):
            self._build_api().list_feeds()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_feed(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_feed method returns the download URL."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_feed.return_value = MagicMock(url="https://feed.example/file")

        result = self._build_api().get_feed("feed-name")

        self.assertEqual("https://feed.example/file", result)
        request = mock_api.get_feed.call_args.kwargs["get_feed_request_content"]
        self.assertEqual("feed-name", request.feed_name)
        self.assertIsNone(request.feed_type)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_feed_with_feed_type(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_feed forwards the feed type to the SDK request."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_feed.return_value = MagicMock(url="https://feed.example/file")

        self._build_api().get_feed("feed-name", feed_type=FeedType.DEALS_FEEDS)

        request = mock_api.get_feed.call_args.kwargs["get_feed_request_content"]
        self.assertEqual(FeedType.DEALS_FEEDS, request.feed_type)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_feed_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_feed raises a wrapped error on API failure."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_feed.side_effect = ApiException(status=404)

        with self.assertRaises(ResourceNotFoundError):
            self._build_api().get_feed("missing-feed")

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_list_reports(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test list_reports method returns the available reports."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        report = MagicMock()
        mock_api.list_reports.return_value = MagicMock(reports=[report])

        result = self._build_api().list_reports()

        self.assertEqual([report], result)
        mock_api.list_reports.assert_called_once_with(
            x_marketplace="www.amazon.es",
            _request_timeout=DEFAULT_TIMEOUT,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_list_reports_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test list_reports raises a wrapped error on API failure."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.list_reports.side_effect = ApiException(status=429)

        with self.assertRaises(TooManyRequestsError):
            self._build_api().list_reports()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_report(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_report method returns the download URL."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_report.return_value = MagicMock(url="https://report.example/file")

        result = self._build_api().get_report("report.csv")

        self.assertEqual("https://report.example/file", result)
        request = mock_api.get_report.call_args.kwargs["get_report_request_content"]
        self.assertEqual("report.csv", request.filename)
        self.assertIsNone(request.report_type)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_report_with_report_type(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_report forwards the report type to the SDK request."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_report.return_value = MagicMock(url="https://report.example/file")

        self._build_api().get_report(
            "report.csv",
            report_type=ReportType.CREATOR_CONNECTIONS,
        )

        request = mock_api.get_report.call_args.kwargs["get_report_request_content"]
        self.assertEqual(ReportType.CREATOR_CONNECTIONS, request.report_type)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_report_api_exception(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_report raises a wrapped error on API failure."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_report.side_effect = ApiException(status=500)

        with self.assertRaises(RequestError):
            self._build_api().get_report("report.csv")

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_with_invalid_timeout(self, _mock_client: MagicMock) -> None:
        """Test that a timeout of zero or below is rejected."""
        for timeout in (0, -1.5):
            with self.assertRaises(InvalidArgumentError):
                AmazonCreatorsApi(
                    credential_id=self.credential_id,
                    credential_secret=self.credential_secret,
                    version=self.version,
                    tag=self.tag,
                    country=self.country,
                    timeout=timeout,
                )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_uses_default_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items forwards the default timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock(asin="B0DLFMFBJW")]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )
        api.get_items(["B0DLFMFBJW"])

        self.assertEqual(api.timeout, DEFAULT_TIMEOUT)
        self.assertEqual(
            mock_api.get_items.call_args.kwargs["_request_timeout"],
            DEFAULT_TIMEOUT,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_forwards_custom_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items forwards a custom timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock(asin="B0DLFMFBJW")]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=15.0,
        )
        api.get_items(["B0DLFMFBJW"])

        self.assertEqual(
            mock_api.get_items.call_args.kwargs["_request_timeout"],
            15.0,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_with_timeout_disabled(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items sends no timeout to the SDK when it is disabled."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock(asin="B0DLFMFBJW")]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=None,
        )
        api.get_items(["B0DLFMFBJW"])

        self.assertIsNone(mock_api.get_items.call_args.kwargs["_request_timeout"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_forwards_custom_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items forwards a custom timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = MagicMock()
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=5.0,
        )
        api.search_items(keywords="laptop")

        self.assertEqual(
            mock_api.search_items.call_args.kwargs["_request_timeout"],
            5.0,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_variations_forwards_custom_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_variations forwards a custom timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.variations_result = MagicMock()
        mock_api.get_variations.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=3.5,
        )
        api.get_variations("B0DLFMFBJW")

        self.assertEqual(
            mock_api.get_variations.call_args.kwargs["_request_timeout"],
            3.5,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_forwards_custom_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes forwards a custom timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.browse_nodes_result.browse_nodes = [MagicMock()]
        mock_api.get_browse_nodes.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=7.5,
        )
        api.get_browse_nodes(["123456"])

        self.assertEqual(
            mock_api.get_browse_nodes.call_args.kwargs["_request_timeout"],
            7.5,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_feed_and_report_methods_forward_timeout(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test feed and report methods forward the timeout to the SDK."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            timeout=9.0,
        )
        api.list_feeds()
        api.get_feed("feed.csv")
        api.list_reports()
        api.get_report("report.csv")

        for call in (
            mock_api.list_feeds,
            mock_api.get_feed,
            mock_api.list_reports,
            mock_api.get_report,
        ):
            self.assertEqual(call.call_args.kwargs["_request_timeout"], 9.0)


class TestAmazonCreatorsApiItems(unittest.TestCase):
    """Tests for the items returned by AmazonCreatorsApi."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"
        self.version = "2.2"
        self.tag = "test-tag"
        self.country: CountryCode = "ES"

    def build_api(self, mock_api_class: MagicMock) -> AmazonCreatorsApi:
        """Build an API client with a mocked SDK."""
        return AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
        )

    def build_response(
        self,
        asins: list[str],
        errors: list[ErrorData] | None = None,
    ) -> GetItemsResponseContent:
        """Build a get items response holding the given items and errors."""
        return GetItemsResponseContent(
            itemsResult=ItemsResult(items=[Item(asin=asin) for asin in asins]),
            errors=errors,
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_keeps_requested_order(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that items are returned in the order they were requested."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = self.build_response(
            ["B000000002", "B000000001"],
        )

        api = self.build_api(mock_api_class)
        result = api.get_items(["B000000001", "B000000002"])

        self.assertEqual([item.asin for item in result], ["B000000001", "B000000002"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_splits_requests_over_the_limit(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that more items than the limit are split into several calls."""
        item_ids = [f"B0000000{index:02d}" for index in range(12)]
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = [
            self.build_response(item_ids[:10]),
            self.build_response(item_ids[10:]),
        ]

        api = self.build_api(mock_api_class)
        result = api.get_items(item_ids)

        self.assertEqual(mock_api.get_items.call_count, 2)
        self.assertEqual([item.asin for item in result], item_ids)
        requests = [
            call.kwargs["get_items_request_content"].item_ids
            for call in mock_api.get_items.call_args_list
        ]
        self.assertEqual([len(request) for request in requests], [10, 2])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_removes_duplicates(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that duplicated items are requested and returned only once."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = self.build_response(["B000000001"])

        api = self.build_api(mock_api_class)
        result = api.get_items(["B000000001", "B000000001"])

        request = mock_api.get_items.call_args.kwargs["get_items_request_content"]
        self.assertEqual(request.item_ids, ["B000000001"])
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_exposes_partial_errors(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that the partial errors of the response are available."""
        error = ErrorData(code="ItemNotFound", message="Item not found")
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = self.build_response(
            ["B000000001"],
            errors=[error],
        )

        api = self.build_api(mock_api_class)
        result = api.get_items(["B000000001", "B000000002"])

        self.assertEqual(result.errors, [error])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_include_unavailable(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that missing items are returned when they are requested."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = self.build_response(["B000000001"])

        api = self.build_api(mock_api_class)
        result = api.get_items(
            ["B000000001", "B000000002"],
            include_unavailable=True,
        )

        self.assertEqual([item.asin for item in result], ["B000000001", "B000000002"])
        self.assertIsNone(result[1].item_info)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_not_found_reports_partial_errors(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that partial errors are reported when nothing is found."""
        error = ErrorData(code="InvalidItemId", message="Item id is invalid")
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = GetItemsResponseContent(errors=[error])

        api = self.build_api(mock_api_class)

        with self.assertRaises(ItemsNotFoundError) as context:
            api.get_items(["B000000001"])

        self.assertIn("InvalidItemId", str(context.exception))

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_invalid_parameter_raises_library_error(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a value rejected by the API raises a library error."""
        api = self.build_api(mock_api_class)

        with self.assertRaises(InvalidArgumentError):
            api.get_items(["B000000001"], languages_of_preference=["es_ES", "en_US"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_browse_nodes_exposes_partial_errors(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that browse nodes expose the partial errors of the response."""
        error = ErrorData(code="InvalidBrowseNodeId", message="Invalid browse node")
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_browse_nodes.return_value = GetBrowseNodesResponseContent(
            browseNodesResult=BrowseNodesResult(browseNodes=[BrowseNode(id="123")]),
            errors=[error],
        )

        api = self.build_api(mock_api_class)
        result = api.get_browse_nodes(["123", "456"])

        self.assertEqual([node.id for node in result], ["123"])
        self.assertEqual(result.errors, [error])

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_token_manager_receives_the_timeout(
        self,
        mock_client_class: MagicMock,
    ) -> None:
        """Test that the token manager is replaced by one with a timeout."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            timeout=12.0,
        )

        token_manager = mock_client._token_manager
        self.assertIsInstance(token_manager, TimeoutOAuth2TokenManager)
        self.assertEqual(token_manager._timeout, 12.0)
        self.assertEqual(api.timeout, 12.0)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items_without_items_raises_library_error(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that requesting no items raises an invalid argument error."""
        api = self.build_api(mock_api_class)

        with self.assertRaises(InvalidArgumentError):
            api.get_items([])


class TestAmazonCreatorsApiRetries(unittest.TestCase):
    """Tests for the retries of AmazonCreatorsApi."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"
        self.version = "2.2"
        self.tag = "test-tag"
        self.country: CountryCode = "ES"

    def build_api(self, retries: int = 2) -> AmazonCreatorsApi:
        """Build an API client with the given amount of retries."""
        return AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=retries,
        )

    def build_response(self) -> GetItemsResponseContent:
        """Build a successful get items response."""
        return GetItemsResponseContent(
            itemsResult=ItemsResult(items=[Item(asin="B000000001")]),
        )

    @mock.patch("amazon_creatorsapi.api.get_retry_delay", return_value=0)
    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_retries_server_errors(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that a server error is retried until it succeeds."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = [
            ApiException(status=500),
            self.build_response(),
        ]

        result = self.build_api().get_items(["B000000001"])

        self.assertEqual(mock_api.get_items.call_count, 2)
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @mock.patch("amazon_creatorsapi.api.get_retry_delay", return_value=0)
    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_stops_after_the_configured_retries(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that the error is raised once the retries are exhausted."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(status=429)

        with self.assertRaises(TooManyRequestsError):
            self.build_api(retries=2).get_items(["B000000001"])

        self.assertEqual(mock_api.get_items.call_count, 3)

    @mock.patch("amazon_creatorsapi.api.get_retry_delay", return_value=0)
    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_honours_the_retry_after_header(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
        mock_delay: MagicMock,
    ) -> None:
        """Test that the headers of the response reach the delay."""
        error = ApiException(status=429)
        error.headers = {"Retry-After": "5"}
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = [error, self.build_response()]

        self.build_api().get_items(["B000000001"])

        mock_delay.assert_called_once_with(0, {"Retry-After": "5"})

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_does_not_retry_client_errors(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a rejected request is not retried."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(status=400)

        with self.assertRaises(InvalidArgumentError):
            self.build_api().get_items(["B000000001"])

        mock_api.get_items.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_refreshes_the_token_once(
        self,
        mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that an expired token is refreshed and the request repeated."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = [
            ApiException(status=401),
            self.build_response(),
        ]

        result = self.build_api(retries=0).get_items(["B000000001"])

        mock_client.token_manager.clear_token.assert_called_once()
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_unauthorized_twice_raises_authentication_error(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a token that stays invalid raises an authentication error."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(status=401)

        with self.assertRaises(AuthenticationError):
            self.build_api(retries=0).get_items(["B000000001"])

        self.assertEqual(mock_api.get_items.call_count, 2)

    @mock.patch("amazon_creatorsapi.api.get_retry_delay", return_value=0)
    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_connection_errors_are_wrapped(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that a connection failure raises a request error."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = urllib3.exceptions.TimeoutError(
            "Read timed out",
        )

        with self.assertRaises(RequestError):
            self.build_api(retries=1).get_items(["B000000001"])

        self.assertEqual(mock_api.get_items.call_count, 2)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_forbidden_raises_access_denied(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a forbidden request raises an access denied error."""
        error = ApiException(status=403)
        error.body = '{"message": "Not eligible", "reason": "AssociateNotEligible"}'
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = error

        with self.assertRaises(AccessDeniedError):
            self.build_api().get_items(["B000000001"])

        mock_api.get_items.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_unauthorized_without_token_manager(
        self,
        mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that the request is repeated even without a cached token."""
        mock_client = MagicMock()
        mock_client.token_manager = None
        mock_client_class.return_value = mock_client
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = [
            ApiException(status=401),
            self.build_response(),
        ]

        result = self.build_api(retries=0).get_items(["B000000001"])

        self.assertEqual([item.asin for item in result], ["B000000001"])

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_negative_retries_are_rejected(self, _mock_client: MagicMock) -> None:
        """Test that a negative amount of retries is rejected."""
        with self.assertRaises(InvalidArgumentError):
            self.build_api(retries=-1)


class TestAmazonCreatorsApiOptions(unittest.TestCase):
    """Tests for the options of AmazonCreatorsApi."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"
        self.version = "2.2"
        self.tag = "test-tag"
        self.country: CountryCode = "ES"

    def build_api(self, **options: object) -> AmazonCreatorsApi:
        """Build an API client with the given options."""
        return AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
            retries=0,
            **options,  # type: ignore[arg-type]
        )

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_forwards_availability(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that the availability filter reaches the SDK request."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.search_items.return_value = MagicMock(search_result=MagicMock())

        self.build_api().search_items(
            keywords="laptop",
            availability=Availability.INCLUDEOUTOFSTOCK,
        )

        request = mock_api.search_items.call_args.kwargs["search_items_request_content"]
        self.assertEqual(request.availability, Availability.INCLUDEOUTOFSTOCK)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items_without_criteria(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a search without criteria does not reach the API."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        with self.assertRaises(InvalidArgumentError):
            self.build_api().search_items()

        mock_api.search_items.assert_not_called()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_errors_report_the_request_id(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that the identifier given by Amazon is part of the error."""
        error = ApiException(status=400)
        error.headers = {"x-amzn-RequestId": "abc-123"}
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = error

        with self.assertRaises(InvalidArgumentError) as context:
            self.build_api().get_items(["B000000001"])

        self.assertIn("abc-123", str(context.exception))

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_custom_host_and_auth_endpoint(self, mock_client_class: MagicMock) -> None:
        """Test that the endpoints of the API can be replaced."""
        self.build_api(
            host="https://example.com",
            auth_endpoint="https://example.com/token",
        )

        options = mock_client_class.call_args.kwargs
        self.assertEqual(options["host"], "https://example.com")
        self.assertEqual(options["auth_endpoint"], "https://example.com/token")

    def test_every_client_has_its_own_configuration(self) -> None:
        """Test that the configuration is not shared between clients."""
        first = self.build_api()
        second = self.build_api()

        self.assertIsNot(
            first._api_client.configuration,
            second._api_client.configuration,
        )

    def build_api_with(self, **options: object) -> AmazonCreatorsApi:
        """Build an API client overriding any of its options."""
        return AmazonCreatorsApi(
            **{  # type: ignore[arg-type]
                "credential_id": self.credential_id,
                "credential_secret": self.credential_secret,
                "version": self.version,
                "tag": self.tag,
                "country": self.country,
                "throttling": 0,
                "retries": 0,
                **options,
            }
        )

    def test_unsupported_version_is_rejected(self) -> None:
        """Test that a version out of the list needs a custom endpoint."""
        with self.assertRaises(ValueError) as context:
            self.build_api_with(version="3.4")

        self.assertIn("Unsupported version: 3.4", str(context.exception))

    def test_unknown_family_is_rejected_with_a_custom_endpoint(self) -> None:
        """Test that a version with an unknown auth flow is always rejected."""
        with self.assertRaises(ValueError) as context:
            self.build_api_with(
                version="4.0",
                auth_endpoint="https://example.com/token",
            )

        self.assertIn("Unsupported version: 4.0", str(context.exception))

    def test_custom_endpoint_accepts_a_new_version(self) -> None:
        """Test that a custom endpoint makes valid a version out of the list."""
        api = self.build_api_with(
            version="3.4",
            auth_endpoint="https://example.com/token",
        )

        token_manager = api._api_client.token_manager
        assert token_manager is not None
        self.assertEqual(
            token_manager.config.get_cognito_endpoint(),
            "https://example.com/token",
        )

    def test_the_endpoint_of_the_version_is_used(self) -> None:
        """Test that the endpoint of the version reaches the token manager."""
        api = self.build_api()

        token_manager = api._api_client.token_manager
        assert token_manager is not None
        self.assertEqual(
            token_manager.config.get_cognito_endpoint(),
            VERSION_ENDPOINTS["2.2"],
        )

    def test_negative_throttling_is_rejected(self) -> None:
        """Test that a negative wait time between calls is rejected."""
        with self.assertRaises(InvalidArgumentError):
            self.build_api_with(throttling=-1)

    def test_throttling_that_is_not_a_number_is_rejected(self) -> None:
        """Test that a wait time that is not a number is rejected."""
        with self.assertRaises(InvalidArgumentError):
            self.build_api_with(throttling="fast")

    def test_close_releases_the_connections(self) -> None:
        """Test that closing the client clears the pool of connections."""
        api = self.build_api()
        api._api_client.rest_client.pool_manager = MagicMock()

        api.close()

        api._api_client.rest_client.pool_manager.clear.assert_called_once()

    def test_context_manager_closes_the_client(self) -> None:
        """Test that leaving the context manager closes the client."""
        api = self.build_api()
        api._api_client.rest_client.pool_manager = MagicMock()

        with api as client:
            self.assertIs(client, api)

        api._api_client.rest_client.pool_manager.clear.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_transport_error_keeps_its_reason(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that an error without a body is reported with its reason."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.side_effect = ApiException(
            status=0,
            reason="SSL error: certificate verify failed",
        )

        with self.assertRaises(RequestError) as context:
            self.build_api().get_items(["B000000001"])

        self.assertIn("certificate verify failed", str(context.exception))

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_items_of_other_asins_are_not_found(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test that a response without any requested item is not found."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.get_items.return_value = GetItemsResponseContent(
            itemsResult=ItemsResult(items=[Item(asin="B000000002")]),
        )

        with self.assertRaises(ItemsNotFoundError):
            self.build_api().get_items(["B000000001"])
