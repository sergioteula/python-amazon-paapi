"""Unit tests for AmazonCreatorsApi class."""

from __future__ import annotations

import time
import unittest
from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import MagicMock

from amazon_creatorsapi import AmazonCreatorsApi
from amazon_creatorsapi.errors import (
    AssociateValidationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    TooManyRequestsError,
)
from creatorsapi_python_sdk.exceptions import ApiException
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource

if TYPE_CHECKING:
    from amazon_creatorsapi.core.marketplaces import CountryCode


class TestAmazonCreatorsApi(unittest.TestCase):
    """Tests for AmazonCreatorsApi class."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"  # noqa: S105
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
        api._last_query_time = time.time()
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
        mock_response.items_result.items = [MagicMock()]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
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
        )
        result = api.search_items(keywords="laptop")
        self.assertIsNotNone(result)
        mock_api.search_items.assert_called_once()

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
        mock_response.items_result.items = [MagicMock()]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
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
        )
        result = api.get_browse_nodes(
            ["123456"],
            resources=[GetBrowseNodesResource.BROWSE_NODES_DOT_ANCESTOR],
        )
        self.assertIsInstance(result, list)
