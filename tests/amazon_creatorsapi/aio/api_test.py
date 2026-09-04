"""Unit tests for AsyncAmazonCreatorsApi class."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from amazon_creatorsapi.aio import (
    AsyncAmazonCreatorsApi,
)
from amazon_creatorsapi.aio.api import API_HOST
from amazon_creatorsapi.core.constants import DEFAULT_TIMEOUT
from amazon_creatorsapi.core.oauth import VERSION_ENDPOINTS
from amazon_creatorsapi.errors import (
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
)
from creatorsapi_python_sdk.models.availability import Availability
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.delivery_flag import DeliveryFlag
from creatorsapi_python_sdk.models.feed_type import FeedType
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from creatorsapi_python_sdk.models.report_type import ReportType
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource
from creatorsapi_python_sdk.models.sort_by import SortBy


class TestAsyncAmazonCreatorsApiInit(unittest.TestCase):
    """Tests for AsyncAmazonCreatorsApi initialization."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_country_code(self, mock_token_manager: MagicMock) -> None:
        """Test initialization with country code."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        )

        self.assertEqual(api.tag, "test-tag")
        self.assertEqual(api.marketplace, "www.amazon.es")
        self.assertEqual(api.throttling, 1.0)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_marketplace(self, mock_token_manager: MagicMock) -> None:
        """Test initialization with explicit marketplace."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            marketplace="www.amazon.co.uk",
        )

        self.assertEqual(api.marketplace, "www.amazon.co.uk")

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_custom_throttling(self, mock_token_manager: MagicMock) -> None:
        """Test initialization with custom throttling value."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="US",
            throttling=2.5,
        )

        self.assertEqual(api.throttling, 2.5)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_default_timeout(self, mock_token_manager: MagicMock) -> None:
        """Test initialization uses the default timeout value."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="US",
        )

        self.assertEqual(api.timeout, DEFAULT_TIMEOUT)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_custom_timeout(self, mock_token_manager: MagicMock) -> None:
        """Test initialization with custom timeout value."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="US",
            timeout=5.0,
        )

        self.assertEqual(api.timeout, 5.0)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_timeout_disabled(self, mock_token_manager: MagicMock) -> None:
        """Test initialization keeps a None timeout to wait indefinitely."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="US",
            timeout=None,
        )

        self.assertIsNone(api.timeout)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_with_invalid_timeout(self, mock_token_manager: MagicMock) -> None:
        """Test initialization rejects a timeout that is not above zero."""
        for timeout in (0, -1.5):
            with self.assertRaises(InvalidArgumentError):
                AsyncAmazonCreatorsApi(
                    credential_id="test_id",
                    credential_secret="test_secret",
                    version="2.2",
                    tag="test-tag",
                    country="US",
                    timeout=timeout,
                )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_timeout_passed_to_token_manager(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test the token manager gets the timeout used for API requests."""
        AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="US",
            timeout=5.0,
        )

        self.assertEqual(mock_token_manager.call_args.kwargs["timeout"], 5.0)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_accepts_lwa_version(self, mock_token_manager: MagicMock) -> None:
        """Test initialization accepts an LWA-backed 3.x version."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="3.1",
            tag="test-tag",
            country="US",
        )

        self.assertEqual(api.marketplace, "www.amazon.com")

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_raises_error_when_no_country_or_marketplace(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test raises InvalidArgumentError when neither country nor marketplace."""
        with self.assertRaises(InvalidArgumentError) as context:
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="2.2",
                tag="test-tag",
            )

        self.assertIn("Either 'country' or 'marketplace'", str(context.exception))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_raises_error_for_invalid_country(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test raises InvalidArgumentError for invalid country code."""
        with self.assertRaises(InvalidArgumentError) as context:
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="2.2",
                tag="test-tag",
                country="XX",  # type: ignore[arg-type]  # Intentionally invalid
            )

        self.assertIn("Country code", str(context.exception))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_raises_error_for_invalid_version(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test raises ValueError for unsupported API version."""
        with self.assertRaises(ValueError) as context:
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="3.9",  # Version out of the list
                tag="test-tag",
                country="ES",
            )

        self.assertIn("Unsupported version: 3.9", str(context.exception))
        self.assertIn("Supported versions are:", str(context.exception))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_raises_error_for_unknown_family(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test that a version with an unknown auth flow is always rejected."""
        with self.assertRaises(ValueError) as context:
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="9.9",  # Family with an unknown auth flow
                tag="test-tag",
                country="ES",
                auth_endpoint="https://example.com/token",
            )

        self.assertIn("Unsupported version: 9.9", str(context.exception))
        mock_token_manager.assert_not_called()

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_custom_endpoint_accepts_a_new_version(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test that a custom endpoint makes valid a version out of the list."""
        AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="3.4",
            tag="test-tag",
            country="ES",
            auth_endpoint="https://example.com/token",
        )

        self.assertEqual(
            mock_token_manager.call_args.kwargs["auth_endpoint"],
            "https://example.com/token",
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_the_endpoint_of_the_version_is_used(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test that the endpoint of the version reaches the token manager."""
        AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        )

        self.assertEqual(
            mock_token_manager.call_args.kwargs["auth_endpoint"],
            VERSION_ENDPOINTS["2.2"],
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_negative_throttling_is_rejected(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test that a negative wait time between calls is rejected."""
        with self.assertRaises(InvalidArgumentError):
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="2.2",
                tag="test-tag",
                country="ES",
                throttling=-1,
            )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    def test_throttling_that_is_not_a_number_is_rejected(
        self, mock_token_manager: MagicMock
    ) -> None:
        """Test that a wait time that is not a number is rejected."""
        with self.assertRaises(InvalidArgumentError):
            AsyncAmazonCreatorsApi(
                credential_id="test_id",
                credential_secret="test_secret",
                version="2.2",
                tag="test-tag",
                country="ES",
                throttling="fast",  # type: ignore[arg-type]
            )


class TestAsyncAmazonCreatorsApiContextManager(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncAmazonCreatorsApi async context manager."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_context_manager_creates_and_closes_client(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager: MagicMock,
    ) -> None:
        """Test context manager creates client on enter and closes on exit."""
        mock_client = AsyncMock()
        mock_http_client_class.return_value = mock_client

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            self.assertTrue(api._owns_client)
            mock_client.__aenter__.assert_called_once()

        mock_client.__aexit__.assert_called_once()

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    async def test_context_manager_exit_without_client(
        self,
        mock_token_manager: MagicMock,
    ) -> None:
        """Test __aexit__ works explicitly when no client initialized."""
        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        )
        # Should not raise
        await api.__aexit__(None, None, None)


class TestAsyncAmazonCreatorsApiGetItems(unittest.IsolatedAsyncioTestCase):
    """Tests for get_items() method."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test successful get_items call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {
                "items": [
                    {
                        "asin": "B0DLFMFBJW",
                        "itemInfo": {"title": {"displayValue": "Test"}},
                    }
                ]
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,  # No throttling for tests
        ) as api:
            items = await api.get_items(["B0DLFMFBJW"])

        self.assertEqual(len(items), 1)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_with_resources(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_items with explicit resources."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            items = await api.get_items(
                ["B0DLFMFBJW"], resources=[GetItemsResource.ITEM_INFO_DOT_TITLE]
            )

        self.assertEqual(len(items), 1)
        # Verify resources were passed
        call_args = mock_client.post.call_args
        self.assertIn("'resources': ['itemInfo.title']", str(call_args))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_items raises ItemsNotFoundError when no items found."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_items(["B0DLFMFBJX"])


class TestAsyncAmazonCreatorsApiSearchItemsDeliveryFlags(
    unittest.IsolatedAsyncioTestCase,
):
    """Focused tests for delivery_flags in search_items()."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_with_delivery_flags(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items includes delivery flags in the request body."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            await api.search_items(
                keywords="laptop",
                delivery_flags=[DeliveryFlag.PRIME, DeliveryFlag.FREESHIPPING],
            )

        call_args = mock_client.post.call_args
        self.assertIn("deliveryFlags", str(call_args))
        self.assertIn("Prime", str(call_args))
        self.assertIn("FreeShipping", str(call_args))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_with_optional_params(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_items with condition, currency, and languages parameters."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            items = await api.get_items(
                items=["B0DLFMFBJW"],
                condition=Condition.NEW,
                currency_of_preference="EUR",
                languages_of_preference=["es_ES"],
            )

        self.assertEqual(len(items), 1)


class TestAsyncAmazonCreatorsApiSearchItems(unittest.IsolatedAsyncioTestCase):
    """Tests for search_items() method."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test successful search_items call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {
                "totalResultCount": 1,
                "items": [{"asin": "B0DLFMFBJY"}],
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.search_items(keywords="test")

        self.assertIsNotNone(result)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_with_resources(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items with explicit resources."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {"items": [{"asin": "B0DLFMFBJY"}]}
        }
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client
        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            await api.search_items(
                keywords="test", resources=[SearchItemsResource.ITEM_INFO_DOT_TITLE]
            )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_without_keywords(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items without keywords (using other params)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {"items": [{"asin": "B0DLFMFBJY"}]}
        }
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client
        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            await api.search_items(browse_node_id="123456")

        call_args = mock_client.post.call_args
        self.assertNotIn("keywords", str(call_args))
        self.assertIn("browseNodeId", str(call_args))


class TestAsyncAmazonCreatorsApiErrorHandling(unittest.IsolatedAsyncioTestCase):
    """Tests for error handling."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_404_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles 404 response correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_items(["B0DLFMFBJW"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_429_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles 429 rate limit response correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(TooManyRequestsError):
                await api.get_items(["B0DLFMFBJW"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_invalid_associate_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles InvalidAssociate error in response body."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "InvalidAssociate: Your credentials are not valid"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(AssociateValidationError):
                await api.get_items(["B0DLFMFBJW"])


class TestAsyncAmazonCreatorsApiThrottling(unittest.IsolatedAsyncioTestCase):
    """Tests for throttling mechanism."""

    @patch("amazon_creatorsapi.aio.api.asyncio.sleep")
    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_throttling_waits_between_requests(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        mock_sleep: MagicMock,
    ) -> None:
        """Test that throttling causes wait between consecutive requests."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJZ"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        mock_sleep.return_value = None

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0.5,
        ) as api:
            await api.get_items(["B0DLFMFBJZ"])
            await api.get_items(["B0DLFMFBJZ"])

        # asyncio.sleep should have been called for throttling
        self.assertTrue(mock_sleep.called)


class TestAsyncAmazonCreatorsApiGetVariations(unittest.IsolatedAsyncioTestCase):
    """Tests for get_variations() method."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_variations_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test successful get_variations call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "variationsResult": {
                "variationSummary": {"pageCount": 1},
                "items": [{"asin": "B0DLFMFBJV"}],
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.get_variations("B0DLFMFBJV")

        self.assertIsNotNone(result)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_variations_with_resources(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_variations with explicit resources."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "variationsResult": {"items": [{"asin": "B0DLFMFBJV"}]}
        }
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client
        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            await api.get_variations(
                "B0DLFMFBJV", resources=[GetVariationsResource.ITEM_INFO_DOT_TITLE]
            )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_variations_with_params(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_variations with optional parameters."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "variationsResult": {
                "variationSummary": {"pageCount": 2},
                "items": [{"asin": "B0DLFMFBJV"}],
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.get_variations(
                asin="B0DLFMFBJV",
                variation_count=5,
                variation_page=1,
                condition=Condition.NEW,
                currency_of_preference="EUR",
                languages_of_preference=["es_ES"],
            )

        self.assertIsNotNone(result)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_variations_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_variations raises ItemsNotFoundError when no variations found."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_variations("B0DLFMFBJV")


class TestAsyncAmazonCreatorsApiGetBrowseNodes(unittest.IsolatedAsyncioTestCase):
    """Tests for get_browse_nodes() method."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test successful get_browse_nodes call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "browseNodesResult": {
                "browseNodes": [{"id": "123456", "displayName": "Electronics"}]
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.get_browse_nodes(["123456"])

        self.assertEqual(len(result), 1)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_with_resources(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes with explicit resources."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "browseNodesResult": {
                "browseNodes": [{"id": "123456", "displayName": "Electronics"}]
            }
        }
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client
        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ) as api:
            await api.get_browse_nodes(
                ["123456"], resources=[GetBrowseNodesResource.BROWSE_NODES_DOT_ANCESTOR]
            )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_with_languages(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes with languages preference."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "browseNodesResult": {
                "browseNodes": [{"id": "123456", "displayName": "Electrónica"}]
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.get_browse_nodes(
                browse_node_ids=["123456"],
                languages_of_preference=["es_ES"],
            )

        self.assertEqual(len(result), 1)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_browse_nodes raises ItemsNotFoundError when no nodes found."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_browse_nodes(["999999"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_empty_nodes_list(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that empty BrowseNodes raises ItemsNotFoundError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"browseNodesResult": {"browseNodes": None}}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_browse_nodes(["123456"])


class TestAsyncAmazonCreatorsApiErrorHandlingExtended(unittest.IsolatedAsyncioTestCase):
    """Extended error handling tests."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_invalid_parameter_value_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles InvalidParameterValue error in response body."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "InvalidParameterValue: The value is not valid"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(InvalidArgumentError):
                await api.get_items(["B0DLFMFBJW"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_invalid_partner_tag_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles InvalidPartnerTag error in response body."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "InvalidPartnerTag: The tag is not valid"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(InvalidArgumentError):
                await api.get_items(["B0DLFMFBJW"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_generic_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles generic error response."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(RequestError):
                await api.get_items(["B0DLFMFBJW"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_handles_generic_error_with_empty_body(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test handles generic error with empty response body."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.text = ""

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(RequestError):
                await api.get_items(["B0DLFMFBJW"])


class TestAsyncAmazonCreatorsApiSearchItemsExtended(unittest.IsolatedAsyncioTestCase):
    """Extended tests for search_items() method."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_with_all_params(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items with all optional parameters."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {
                "totalResultCount": 10,
                "items": [{"asin": "B0DLFMFBJY"}],
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.search_items(
                keywords="laptop",
                actor="actor",
                artist="artist",
                author="author",
                brand="brand",
                browse_node_id="123",
                condition=Condition.NEW,
                currency_of_preference="EUR",
                item_count=10,
                item_page=1,
                languages_of_preference=["es_ES"],
                max_price=10000,
                min_price=100,
                min_reviews_rating=4,
                min_saving_percent=10,
                sort_by=SortBy.PRICE_COLON_LOW_TO_HIGH,
                title="laptop",
            )

        self.assertIsNotNone(result)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items raises ItemsNotFoundError when no results."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.search_items(keywords="xyznonexistent123")

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_with_search_index(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test search_items with search_index parameter."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "searchResult": {
                "totalResultCount": 1,
                "items": [{"asin": "B0DLFMFBJY"}],
            }
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        ) as api:
            result = await api.search_items(
                keywords="laptop",
                search_index="Electronics",
            )

        self.assertIsNotNone(result)


class TestAsyncAmazonCreatorsApiWithoutContextManager(unittest.IsolatedAsyncioTestCase):
    """Tests for usage without context manager."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_request_without_context_manager(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test making request without context manager creates temp client."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

        items = await api.get_items(["B0DLFMFBJW"])

        self.assertEqual(len(items), 1)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_request_uses_v2_authorization_header(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test v2 requests include the version suffix in Authorization."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

        await api.get_items(["B0DLFMFBJW"])

        headers = mock_client.post.call_args.args[1]
        self.assertEqual(headers["Authorization"], "Bearer test_token, Version 2.2")

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_request_uses_lwa_authorization_header(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test v3 requests omit the version suffix in Authorization."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="3.1",
            tag="test-tag",
            country="US",
            throttling=0,
            retries=0,
        )

        await api.get_items(["B0DLFMFBJW"])

        headers = mock_client.post.call_args.args[1]
        self.assertEqual(headers["Authorization"], "Bearer test_token")


class TestAsyncAmazonCreatorsApiFeeds(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncAmazonCreatorsApi feed operations."""

    def _mock_transport(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        payload: dict,
    ) -> AsyncMock:
        """Wire the HTTP client and token manager mocks to return a payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = payload

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        return mock_client

    def _build_api(self) -> AsyncAmazonCreatorsApi:
        """Build an API instance with throttling disabled."""
        return AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_list_feeds_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test list_feeds returns deserialized feeds."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {
                "feeds": [
                    {
                        "feedName": "product-feed",
                        "size": 1024,
                        "md5": "abc123",
                        "lastUpdated": "2026-09-01T00:00:00Z",
                        "feedType": "PRODUCT_FEEDS",
                    }
                ]
            },
        )

        async with self._build_api() as api:
            feeds = await api.list_feeds()

        self.assertEqual(1, len(feeds))
        self.assertEqual("product-feed", feeds[0].feed_name)
        self.assertEqual(FeedType.PRODUCT_FEEDS, feeds[0].feed_type)
        self.assertEqual("/catalog/v1/listFeeds", mock_client.post.call_args.args[0])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_list_feeds_without_feeds(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test list_feeds returns an empty list when no feeds are available."""
        self._mock_transport(mock_http_client_class, mock_token_manager_class, {})

        async with self._build_api() as api:
            self.assertEqual([], await api.list_feeds())

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_feed_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_feed returns the download URL without a feed type."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {"url": "https://feed.example/file"},
        )

        async with self._build_api() as api:
            url = await api.get_feed("product-feed")

        self.assertEqual("https://feed.example/file", url)
        self.assertEqual(
            {"feedName": "product-feed"},
            mock_client.post.call_args.args[2],
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_feed_with_feed_type(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_feed sends the feed type in the request body."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {"url": "https://feed.example/file"},
        )

        async with self._build_api() as api:
            await api.get_feed("deals-feed", feed_type=FeedType.DEALS_FEEDS)

        self.assertEqual(
            {"feedName": "deals-feed", "feedType": "DEALS_FEEDS"},
            mock_client.post.call_args.args[2],
        )


class TestAsyncAmazonCreatorsApiReports(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncAmazonCreatorsApi report operations."""

    def _mock_transport(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        payload: dict,
    ) -> AsyncMock:
        """Wire the HTTP client and token manager mocks to return a payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = payload

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        return mock_client

    def _build_api(self) -> AsyncAmazonCreatorsApi:
        """Build an API instance with throttling disabled."""
        return AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_list_reports_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test list_reports returns deserialized reports."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {
                "reports": [
                    {
                        "filename": "earnings.csv",
                        "md5": "abc123",
                        "size": 2048,
                        "lastModified": "2026-09-01T00:00:00Z",
                        "reportType": "CREATOR_CONNECTIONS",
                    }
                ]
            },
        )

        async with self._build_api() as api:
            reports = await api.list_reports()

        self.assertEqual(1, len(reports))
        self.assertEqual("earnings.csv", reports[0].filename)
        self.assertEqual(ReportType.CREATOR_CONNECTIONS, reports[0].report_type)
        self.assertEqual("/reports/v1/listReports", mock_client.post.call_args.args[0])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_list_reports_without_reports(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test list_reports returns an empty list when no reports exist."""
        self._mock_transport(mock_http_client_class, mock_token_manager_class, {})

        async with self._build_api() as api:
            self.assertEqual([], await api.list_reports())

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_report_success(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_report returns the download URL without a report type."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {"url": "https://report.example/file"},
        )

        async with self._build_api() as api:
            url = await api.get_report("earnings.csv")

        self.assertEqual("https://report.example/file", url)
        self.assertEqual(
            {"filename": "earnings.csv"},
            mock_client.post.call_args.args[2],
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_report_with_report_type(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test get_report sends the report type in the request body."""
        mock_client = self._mock_transport(
            mock_http_client_class,
            mock_token_manager_class,
            {"url": "https://report.example/file"},
        )

        async with self._build_api() as api:
            await api.get_report(
                "earnings.csv",
                report_type=ReportType.CREATOR_CENTRAL,
            )

        self.assertEqual(
            {"filename": "earnings.csv", "reportType": "CREATOR_CENTRAL"},
            mock_client.post.call_args.args[2],
        )


class TestAsyncAmazonCreatorsApiTimeout(unittest.IsolatedAsyncioTestCase):
    """Tests for the timeout given to the underlying HTTP client."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_context_manager_client_uses_default_timeout(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager: MagicMock,
    ) -> None:
        """Test the persistent client is created with the default timeout."""
        mock_http_client_class.return_value = AsyncMock()

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
        ):
            pass

        mock_http_client_class.assert_called_once_with(
            host=API_HOST,
            timeout=DEFAULT_TIMEOUT,
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_context_manager_client_uses_custom_timeout(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager: MagicMock,
    ) -> None:
        """Test the persistent client is created with a custom timeout."""
        mock_http_client_class.return_value = AsyncMock()

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            timeout=5.0,
        ):
            pass

        mock_http_client_class.assert_called_once_with(host=API_HOST, timeout=5.0)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_request_without_context_manager_uses_custom_timeout(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test the temporary client is created with a custom timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B0DLFMFBJW"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
            timeout=5.0,
        )

        await api.get_items(["B0DLFMFBJW"])

        mock_http_client_class.assert_called_once_with(host=API_HOST, timeout=5.0)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_client_receives_disabled_timeout(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager: MagicMock,
    ) -> None:
        """Test a None timeout is passed to the HTTP client to disable it."""
        mock_http_client_class.return_value = AsyncMock()

        async with AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            timeout=None,
        ):
            pass

        mock_http_client_class.assert_called_once_with(host=API_HOST, timeout=None)


class TestAsyncAmazonCreatorsApiItems(unittest.IsolatedAsyncioTestCase):
    """Tests for the items returned by AsyncAmazonCreatorsApi."""

    def build_client(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        payloads: list[dict],
    ) -> AsyncMock:
        """Prepare the mocked HTTP client with the given response payloads."""
        responses = []
        for payload in payloads:
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = payload
            responses.append(response)

        mock_client = AsyncMock()
        mock_client.post.side_effect = responses
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        return mock_client

    def build_api(self) -> AsyncAmazonCreatorsApi:
        """Build an async API client for the tests."""
        return AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

    def build_payload(
        self,
        asins: list[str],
        errors: list[dict] | None = None,
    ) -> dict:
        """Build a get items response payload."""
        payload: dict = {"itemsResult": {"items": [{"asin": asin} for asin in asins]}}
        if errors is not None:
            payload["errors"] = errors
        return payload

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_keeps_requested_order(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that items are returned in the order they were requested."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_payload(["B000000002", "B000000001"])],
        )

        result = await self.build_api().get_items(["B000000001", "B000000002"])

        self.assertEqual([item.asin for item in result], ["B000000001", "B000000002"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_splits_requests_over_the_limit(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that more items than the limit are split into several calls."""
        item_ids = [f"B0000000{index:02d}" for index in range(12)]
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [
                self.build_payload(item_ids[:10]),
                self.build_payload(item_ids[10:]),
            ],
        )

        result = await self.build_api().get_items(item_ids)

        self.assertEqual(mock_client.post.await_count, 2)
        self.assertEqual([item.asin for item in result], item_ids)
        sent = [call.args[2]["itemIds"] for call in mock_client.post.await_args_list]
        self.assertEqual([len(chunk) for chunk in sent], [10, 2])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_removes_duplicates(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that duplicated items are requested and returned only once."""
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_payload(["B000000001"])],
        )

        result = await self.build_api().get_items(["B000000001", "B000000001"])

        self.assertEqual(mock_client.post.await_args.args[2]["itemIds"], ["B000000001"])
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_exposes_partial_errors(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that the partial errors of the response are available."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [
                self.build_payload(
                    ["B000000001"],
                    errors=[{"code": "ItemNotFound", "message": "Item not found"}],
                )
            ],
        )

        result = await self.build_api().get_items(["B000000001", "B000000002"])

        self.assertEqual([error.code for error in result.errors], ["ItemNotFound"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_include_unavailable(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that missing items are returned when they are requested."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_payload(["B000000001"])],
        )

        result = await self.build_api().get_items(
            ["B000000001", "B000000002"],
            include_unavailable=True,
        )

        self.assertEqual([item.asin for item in result], ["B000000001", "B000000002"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_not_found_reports_partial_errors(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that partial errors are reported when nothing is found."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [{"errors": [{"code": "InvalidItemId", "message": "Invalid item"}]}],
        )

        with self.assertRaises(ItemsNotFoundError) as context:
            await self.build_api().get_items(["B000000001"])

        self.assertIn("InvalidItemId", str(context.exception))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_browse_nodes_exposes_partial_errors(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that browse nodes expose the partial errors of the response."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [
                {
                    "browseNodesResult": {"browseNodes": [{"id": "123"}]},
                    "errors": [{"code": "InvalidBrowseNodeId", "message": "Invalid"}],
                }
            ],
        )

        result = await self.build_api().get_browse_nodes(["123", "456"])

        self.assertEqual([node.id for node in result], ["123"])
        self.assertEqual(
            [error.code for error in result.errors],
            ["InvalidBrowseNodeId"],
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_get_items_without_items_raises_library_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that requesting no items raises an invalid argument error."""
        self.build_client(mock_http_client_class, mock_token_manager_class, [])

        with self.assertRaises(InvalidArgumentError):
            await self.build_api().get_items([])


class TestAsyncAmazonCreatorsApiRetries(unittest.IsolatedAsyncioTestCase):
    """Tests for the retries of AsyncAmazonCreatorsApi."""

    def build_client(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        responses: list[MagicMock | Exception],
    ) -> tuple[AsyncMock, AsyncMock]:
        """Prepare the mocked HTTP client with the given responses."""
        mock_client = AsyncMock()
        mock_client.post.side_effect = responses
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        # clear_token is not a coroutine in the token manager
        mock_token_manager.clear_token = MagicMock()
        mock_token_manager_class.return_value = mock_token_manager

        return mock_client, mock_token_manager

    def build_response(
        self,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ) -> MagicMock:
        """Build a response of the API with the given status."""
        response = MagicMock()
        response.status_code = status_code
        response.headers = headers or {}
        response.text = '{"message": "error"}'
        response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B000000001"}]}
        }
        return response

    def build_api(self, retries: int = 2) -> AsyncAmazonCreatorsApi:
        """Build an async API client with the given amount of retries."""
        return AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=retries,
        )

    @patch("amazon_creatorsapi.aio.api.get_retry_delay", return_value=0)
    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_retries_server_errors(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that a server error is retried until it succeeds."""
        mock_client, _ = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_response(500), self.build_response()],
        )

        result = await self.build_api().get_items(["B000000001"])

        self.assertEqual(mock_client.post.await_count, 2)
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @patch("amazon_creatorsapi.aio.api.get_retry_delay", return_value=0)
    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_stops_after_the_configured_retries(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that the error is raised once the retries are exhausted."""
        mock_client, _ = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_response(429) for _ in range(3)],
        )

        with self.assertRaises(TooManyRequestsError):
            await self.build_api(retries=2).get_items(["B000000001"])

        self.assertEqual(mock_client.post.await_count, 3)

    @patch("amazon_creatorsapi.aio.api.get_retry_delay", return_value=0)
    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_honours_the_retry_after_header(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        mock_delay: MagicMock,
    ) -> None:
        """Test that the headers of the response reach the delay."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [
                self.build_response(503, headers={"retry-after": "5"}),
                self.build_response(),
            ],
        )

        await self.build_api().get_items(["B000000001"])

        mock_delay.assert_called_once_with(0, {"retry-after": "5"})

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_refreshes_the_token_once(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that an expired token is refreshed and the request repeated."""
        _, mock_token_manager = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_response(401), self.build_response()],
        )

        result = await self.build_api(retries=0).get_items(["B000000001"])

        mock_token_manager.clear_token.assert_called_once()
        self.assertEqual([item.asin for item in result], ["B000000001"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_unauthorized_twice_raises_authentication_error(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a token that stays invalid raises an authentication error."""
        mock_client, _ = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_response(401), self.build_response(401)],
        )

        with self.assertRaises(AuthenticationError):
            await self.build_api(retries=0).get_items(["B000000001"])

        self.assertEqual(mock_client.post.await_count, 2)

    @patch("amazon_creatorsapi.aio.api.get_retry_delay", return_value=0)
    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_connection_errors_are_wrapped(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        _mock_delay: MagicMock,
    ) -> None:
        """Test that a connection failure raises a request error."""
        mock_client, _ = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [httpx.ConnectTimeout("timed out"), httpx.ConnectTimeout("timed out")],
        )

        with self.assertRaises(RequestError):
            await self.build_api(retries=1).get_items(["B000000001"])

        self.assertEqual(mock_client.post.await_count, 2)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_invalid_json_is_wrapped(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a response that is not JSON raises a request error."""
        response = self.build_response()
        response.json.side_effect = ValueError("no json")
        self.build_client(mock_http_client_class, mock_token_manager_class, [response])

        with self.assertRaises(RequestError):
            await self.build_api(retries=0).get_items(["B000000001"])

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_missing_report_raises_resource_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a missing report is told apart from missing items."""
        self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
            [self.build_response(404)],
        )

        with self.assertRaises(ResourceNotFoundError):
            await self.build_api(retries=0).get_report("missing.csv")

    def test_negative_retries_are_rejected(self) -> None:
        """Test that a negative amount of retries is rejected."""
        with self.assertRaises(InvalidArgumentError):
            self.build_api(retries=-1)


class TestAsyncAmazonCreatorsApiOptions(unittest.IsolatedAsyncioTestCase):
    """Tests for the options of AsyncAmazonCreatorsApi."""

    def build_client(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
        payload: dict | None = None,
    ) -> AsyncMock:
        """Prepare the mocked HTTP client with a successful response."""
        response = MagicMock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = payload or {
            "searchResult": {"totalResultCount": 1}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager.clear_token = MagicMock()
        mock_token_manager_class.return_value = mock_token_manager

        return mock_client

    def build_api(self, **options: object) -> AsyncAmazonCreatorsApi:
        """Build an async API client with the given options."""
        return AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
            **options,  # type: ignore[arg-type]
        )

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_forwards_availability(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that the availability filter is sent to the API."""
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
        )

        await self.build_api().search_items(
            keywords="laptop",
            availability=Availability.INCLUDEOUTOFSTOCK,
        )

        body = mock_client.post.await_args.args[2]
        self.assertEqual(body["availability"], "IncludeOutOfStock")

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_search_items_without_criteria(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a search without criteria does not reach the API."""
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
        )

        with self.assertRaises(InvalidArgumentError):
            await self.build_api().search_items()

        mock_client.post.assert_not_awaited()

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_request_body_uses_the_names_of_the_api(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that the body is built from the models of the SDK."""
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
        )

        await self.build_api().search_items(
            keywords="laptop",
            browse_node_id="123",
            sort_by=SortBy.PRICE_COLON_LOW_TO_HIGH,
            resources=[SearchItemsResource.ITEM_INFO_DOT_TITLE],
        )

        body = mock_client.post.await_args.args[2]
        self.assertEqual(body["browseNodeId"], "123")
        self.assertEqual(body["sortBy"], "Price:LowToHigh")
        self.assertEqual(body["resources"], ["itemInfo.title"])
        self.assertNotIn("actor", body)

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_invalid_value_does_not_reach_the_api(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a value rejected by the API is caught before sending it."""
        mock_client = self.build_client(
            mock_http_client_class,
            mock_token_manager_class,
        )

        with self.assertRaises(InvalidArgumentError):
            await self.build_api().search_items(keywords="laptop", min_reviews_rating=5)

        mock_client.post.assert_not_awaited()

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_errors_report_the_request_id(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that the identifier given by Amazon is part of the error."""
        response = MagicMock()
        response.status_code = 400
        response.headers = {"x-amzn-RequestId": "abc-123"}
        response.text = '{"message": "invalid"}'

        mock_client = AsyncMock()
        mock_client.post.return_value = response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        with self.assertRaises(InvalidArgumentError) as context:
            await self.build_api().search_items(keywords="laptop")

        self.assertIn("abc-123", str(context.exception))

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_custom_host_and_auth_endpoint(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that the endpoints of the API can be replaced."""
        self.build_client(mock_http_client_class, mock_token_manager_class)

        api = self.build_api(
            host="https://example.com",
            auth_endpoint="https://example.com/token",
        )
        await api.search_items(keywords="laptop")

        self.assertEqual(
            mock_token_manager_class.call_args.kwargs["auth_endpoint"],
            "https://example.com/token",
        )
        self.assertEqual(
            mock_http_client_class.call_args.kwargs["host"],
            "https://example.com",
        )


class TestAsyncAmazonCreatorsApiUnrequestedItems(unittest.IsolatedAsyncioTestCase):
    """Tests for a response holding items that were not requested."""

    @patch("amazon_creatorsapi.aio.api.AsyncOAuth2TokenManager")
    @patch("amazon_creatorsapi.aio.api.AsyncHttpClient")
    async def test_items_of_other_asins_are_not_found(
        self,
        mock_http_client_class: MagicMock,
        mock_token_manager_class: MagicMock,
    ) -> None:
        """Test that a response without any requested item is not found."""
        response = MagicMock()
        response.status_code = 200
        response.headers = {}
        response.json.return_value = {
            "itemsResult": {"items": [{"asin": "B000000002"}]}
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = response
        mock_client.__aenter__.return_value = mock_client
        mock_http_client_class.return_value = mock_client

        mock_token_manager = AsyncMock()
        mock_token_manager.get_token.return_value = "test_token"
        mock_token_manager_class.return_value = mock_token_manager

        api = AsyncAmazonCreatorsApi(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            tag="test-tag",
            country="ES",
            throttling=0,
            retries=0,
        )

        with self.assertRaises(ItemsNotFoundError):
            await api.get_items(["B000000001"])


if __name__ == "__main__":
    unittest.main()
