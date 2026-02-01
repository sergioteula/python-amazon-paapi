"""Unit tests for async HTTP client."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from amazon_creatorsapi.core.async_client import (
    DEFAULT_HOST,
    DEFAULT_TIMEOUT,
    USER_AGENT,
    AsyncHttpClient,
    AsyncHttpResponse,
)


class TestAsyncHttpResponse(unittest.TestCase):
    """Tests for AsyncHttpResponse dataclass."""

    def test_json_parsing(self) -> None:
        """Test that json() correctly parses response body."""
        response = AsyncHttpResponse(
            status_code=200,
            headers={"content-type": "application/json"},
            body=b'{"key": "value"}',
            text='{"key": "value"}',
        )

        result = response.json()

        self.assertEqual(result, {"key": "value"})

    def test_attributes(self) -> None:
        """Test that all attributes are correctly set."""
        response = AsyncHttpResponse(
            status_code=404,
            headers={"x-custom": "header"},
            body=b"test body",
            text="test body",
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers, {"x-custom": "header"})
        self.assertEqual(response.body, b"test body")
        self.assertEqual(response.text, "test body")


class TestAsyncHttpClientInit(unittest.TestCase):
    """Tests for AsyncHttpClient initialization."""

    def test_default_values(self) -> None:
        """Test that default values are correctly set."""
        client = AsyncHttpClient()

        self.assertEqual(client._host, DEFAULT_HOST)
        self.assertEqual(client._timeout, DEFAULT_TIMEOUT)
        self.assertIsNone(client._client)
        self.assertFalse(client._owns_client)

    def test_custom_values(self) -> None:
        """Test that custom values are correctly set."""
        client = AsyncHttpClient(
            host="https://custom.host",
            timeout=60.0,
        )

        self.assertEqual(client._host, "https://custom.host")
        self.assertEqual(client._timeout, 60.0)


class TestAsyncHttpClientContextManager(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncHttpClient async context manager."""

    @patch("amazon_creatorsapi.core.async_client.httpx.AsyncClient")
    async def test_aenter_creates_client(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test that __aenter__ creates an httpx.AsyncClient."""
        mock_client = AsyncMock()
        mock_async_client_class.return_value = mock_client

        client = AsyncHttpClient()

        result = await client.__aenter__()

        mock_async_client_class.assert_called_once()
        self.assertIs(result, client)
        self.assertTrue(client._owns_client)

    @patch("amazon_creatorsapi.core.async_client.httpx.AsyncClient")
    async def test_aexit_closes_client(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test that __aexit__ closes the client."""
        mock_client = AsyncMock()
        mock_async_client_class.return_value = mock_client

        client = AsyncHttpClient()
        await client.__aenter__()
        await client.__aexit__(None, None, None)

        mock_client.aclose.assert_called_once()
        self.assertIsNone(client._client)
        self.assertFalse(client._owns_client)


class TestAsyncHttpClientPost(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncHttpClient.post() method."""

    @patch("amazon_creatorsapi.core.async_client.httpx.AsyncClient")
    async def test_post_with_context_manager(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test POST request using context manager (persistent client)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.content = b'{"result": "ok"}'
        mock_response.text = '{"result": "ok"}'

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_async_client_class.return_value = mock_client

        async with AsyncHttpClient() as client:
            response = await client.post(
                "/test/path",
                {"Authorization": "Bearer token"},
                {"data": "value"},
            )

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        self.assertEqual(call_args[0][0], "/test/path")
        self.assertIn("Authorization", call_args[1]["headers"])
        self.assertIn(USER_AGENT, call_args[1]["headers"]["User-Agent"])
        self.assertEqual(call_args[1]["json"], {"data": "value"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "ok"})

    @patch("amazon_creatorsapi.core.async_client.httpx.AsyncClient")
    async def test_post_without_context_manager(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test POST request without context manager (creates new client)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.content = b'{"standalone": true}'
        mock_response.text = '{"standalone": true}'

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        client = AsyncHttpClient()
        response = await client.post("/test", {}, {"query": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"standalone": True})


if __name__ == "__main__":
    unittest.main()
