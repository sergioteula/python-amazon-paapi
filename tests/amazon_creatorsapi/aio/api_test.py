"""Unit tests for AsyncAmazonCreatorsApi class."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from amazon_creatorsapi.aio import (
    AsyncAmazonCreatorsApi,
)
from amazon_creatorsapi.errors import (
    AssociateValidationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    TooManyRequestsError,
)
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.get_browse_nodes_resource import (
    GetBrowseNodesResource,
)
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
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
                        "ASIN": "B0DLFMFBJW",
                        "ItemInfo": {"Title": {"DisplayValue": "Test"}},
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
            "itemsResult": {"items": [{"ASIN": "B0DLFMFBJW"}]}
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
        ) as api:
            with self.assertRaises(ItemsNotFoundError):
                await api.get_items(["B0DLFMFBJX"])

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
            "itemsResult": {"items": [{"ASIN": "B0DLFMFBJW"}]}
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
                "TotalResultCount": 1,
                "items": [{"ASIN": "B0DLFMFBJY"}],
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
            "searchResult": {"items": [{"ASIN": "B0DLFMFBJY"}]}
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
            "searchResult": {"items": [{"ASIN": "B0DLFMFBJY"}]}
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
            "itemsResult": {"items": [{"ASIN": "B0DLFMFBJZ"}]}
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
            await api.get_items(["B0DLFMFBJ1"])
            await api.get_items(["B0DLFMFBJ2"])

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
                "VariationSummary": {"PageCount": 1},
                "items": [{"ASIN": "B0DLFMFBJV"}],
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
            "variationsResult": {"items": [{"ASIN": "B0DLFMFBJV"}]}
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
                "VariationSummary": {"PageCount": 2},
                "items": [{"ASIN": "B0DLFMFBJV"}],
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
                "browseNodes": [{"Id": "123456", "DisplayName": "Electronics"}]
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
                "browseNodes": [{"Id": "123456", "DisplayName": "Electronics"}]
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
                "browseNodes": [{"Id": "123456", "DisplayName": "Electrónica"}]
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
                "TotalResultCount": 10,
                "items": [{"ASIN": "B0DLFMFBJY"}],
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
                "TotalResultCount": 1,
                "items": [{"ASIN": "B0DLFMFBJY"}],
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
            "itemsResult": {"items": [{"ASIN": "B0DLFMFBJW"}]}
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
        )

        items = await api.get_items(["B0DLFMFBJW"])

        self.assertEqual(len(items), 1)


if __name__ == "__main__":
    unittest.main()
