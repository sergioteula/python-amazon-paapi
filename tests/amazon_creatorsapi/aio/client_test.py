"""Unit tests for AsyncHttpClient."""

import subprocess
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from amazon_creatorsapi.aio.client import (
    DEFAULT_HOST,
    DEFAULT_TIMEOUT,
    AsyncHttpClient,
    AsyncHttpResponse,
)


class TestAsyncHttpClient(unittest.IsolatedAsyncioTestCase):
    """Tests for AsyncHttpClient."""

    async def test_init_defaults(self) -> None:
        """Test initialization with default values."""
        client = AsyncHttpClient()
        self.assertEqual(client._host, DEFAULT_HOST)
        self.assertEqual(client._timeout, DEFAULT_TIMEOUT)
        self.assertIsNone(client._client)
        self.assertFalse(client._owns_client)

    async def test_init_custom(self) -> None:
        """Test initialization with custom values."""
        host = "https://custom.host"
        timeout = 60.0
        client = AsyncHttpClient(host=host, timeout=timeout)
        self.assertEqual(client._host, host)
        self.assertEqual(client._timeout, timeout)

    @patch("amazon_creatorsapi.aio.client.httpx.AsyncClient")
    async def test_context_manager(self, mock_client_cls: MagicMock) -> None:
        """Test context manager creates and closes client."""
        mock_client_instance = AsyncMock()
        mock_client_cls.return_value = mock_client_instance

        async with AsyncHttpClient() as client:
            self.assertTrue(client._owns_client)
            self.assertEqual(client._client, mock_client_instance)
            mock_client_cls.assert_called_once()

        mock_client_instance.aclose.assert_called_once()
        self.assertFalse(client._owns_client)
        self.assertIsNone(client._client)

    @patch("amazon_creatorsapi.aio.client.httpx.AsyncClient")
    async def test_info_logging_context_manager(
        self, mock_client_cls: MagicMock
    ) -> None:
        """Test __aexit__ does nothing if client is None or not owned."""
        client = AsyncHttpClient()
        await client.__aexit__(None, None, None)
        # Should not raise

        client._owns_client = True
        await client.__aexit__(None, None, None)
        # client is None, so nothing happens

    @patch("amazon_creatorsapi.aio.client.httpx.AsyncClient")
    async def test_post_without_context_manager(
        self, mock_client_cls: MagicMock
    ) -> None:
        """Test post request creates temporary client."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"key": "value"}'
        mock_response.text = '{"key": "value"}'

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_cls.return_value = mock_client_instance

        client = AsyncHttpClient()
        response = await client.post("/test", {}, {})

        self.assertIsInstance(response, AsyncHttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

        # Verify temporary client usage
        mock_client_cls.assert_called()
        mock_client_instance.__aenter__.assert_called()
        mock_client_instance.__aexit__.assert_called()

    @patch("amazon_creatorsapi.aio.client.httpx.AsyncClient")
    async def test_post_with_context_manager(self, mock_client_cls: MagicMock) -> None:
        """Test post request reuses existing client."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = b"{}"
        mock_response.text = "{}"

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client_cls.return_value = mock_client_instance

        async with AsyncHttpClient() as client:
            mock_client_cls.reset_mock()  # Reset call from __aenter__
            await client.post("/test", {}, {})

            # Should NOT create new client
            mock_client_cls.assert_not_called()
            # Should call post on existing instance
            mock_client_instance.post.assert_called_once()


class TestAsyncHttpResponse(unittest.TestCase):
    """Tests for AsyncHttpResponse."""

    def test_json_parsing(self) -> None:
        """Test json parsing method."""
        response = AsyncHttpResponse(
            status_code=200, headers={}, body=b'{"foo": "bar"}', text='{"foo": "bar"}'
        )
        self.assertEqual(response.json(), {"foo": "bar"})


class TestAsyncModuleInit(unittest.TestCase):
    """Test async module initialization logic."""

    def test_httpx_import_error(self) -> None:
        """Test ImportError raised when httpx missing."""

        code = """
import sys
# Mock httpx as None in sys.modules to simulate it being missing
sys.modules['httpx'] = None
try:
    import amazon_creatorsapi.aio
except ImportError as e:
    if "httpx is required" in str(e):
        sys.exit(0)
    print(f"Wrong error message: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Wrong exception type: {type(e)}")
    sys.exit(1)
else:
    print("No exception raised")
    sys.exit(1)
"""
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=str(sys.path[0]),  # Ensure we can import the package
            check=False,
        )
        self.assertEqual(
            result.returncode, 0, f"Subprocess failed: {result.stdout} {result.stderr}"
        )
