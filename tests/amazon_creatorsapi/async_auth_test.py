"""Unit tests for async OAuth2 token manager."""

import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from amazon_creatorsapi.core.async_auth import (
    GRANT_TYPE,
    SCOPE,
    TOKEN_EXPIRATION_BUFFER,
    VERSION_ENDPOINTS,
    AsyncOAuth2TokenManager,
)
from amazon_creatorsapi.errors import AuthenticationError


class TestAsyncOAuth2TokenManagerInit(unittest.TestCase):
    """Tests for AsyncOAuth2TokenManager initialization."""

    def test_with_version_21(self) -> None:
        """Test initialization with version 2.1."""
        manager = AsyncOAuth2TokenManager(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.1",
        )

        self.assertEqual(manager._credential_id, "test_id")
        self.assertEqual(manager._credential_secret, "test_secret")
        self.assertEqual(manager._version, "2.1")
        self.assertEqual(manager._auth_endpoint, VERSION_ENDPOINTS["2.1"])

    def test_with_version_22(self) -> None:
        """Test initialization with version 2.2."""
        manager = AsyncOAuth2TokenManager(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
        )

        self.assertEqual(manager._auth_endpoint, VERSION_ENDPOINTS["2.2"])

    def test_with_version_23(self) -> None:
        """Test initialization with version 2.3."""
        manager = AsyncOAuth2TokenManager(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.3",
        )

        self.assertEqual(manager._auth_endpoint, VERSION_ENDPOINTS["2.3"])

    def test_with_custom_endpoint(self) -> None:
        """Test initialization with custom auth endpoint."""
        custom_endpoint = "https://custom.auth.endpoint/token"
        manager = AsyncOAuth2TokenManager(
            credential_id="test_id",
            credential_secret="test_secret",
            version="2.2",
            auth_endpoint=custom_endpoint,
        )

        self.assertEqual(manager._auth_endpoint, custom_endpoint)

    def test_with_invalid_version(self) -> None:
        """Test initialization with unsupported version raises ValueError."""
        with self.assertRaises(ValueError) as context:
            AsyncOAuth2TokenManager(
                credential_id="test_id",
                credential_secret="test_secret",
                version="1.0",
            )

        self.assertIn("Unsupported version", str(context.exception))


class TestAsyncOAuth2TokenManagerIsTokenValid(unittest.TestCase):
    """Tests for is_token_valid() method."""

    def test_returns_false_when_no_token(self) -> None:
        """Test returns False when no token is cached."""
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")

        self.assertFalse(manager.is_token_valid())

    def test_returns_false_when_token_expired(self) -> None:
        """Test returns False when token has expired."""
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")
        manager._access_token = "expired_token"
        manager._expires_at = time.time() - 100  # Expired 100 seconds ago

        self.assertFalse(manager.is_token_valid())

    def test_returns_true_when_token_valid(self) -> None:
        """Test returns True when token is valid and not expired."""
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")
        manager._access_token = "valid_token"
        manager._expires_at = time.time() + 3600  # Expires in 1 hour

        self.assertTrue(manager.is_token_valid())


class TestAsyncOAuth2TokenManagerClearToken(unittest.TestCase):
    """Tests for clear_token() method."""

    def test_clears_token_and_expiration(self) -> None:
        """Test that clear_token clears both token and expiration."""
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")
        manager._access_token = "some_token"
        manager._expires_at = time.time() + 3600

        manager.clear_token()

        self.assertIsNone(manager._access_token)
        self.assertIsNone(manager._expires_at)


class TestAsyncOAuth2TokenManagerGetToken(unittest.IsolatedAsyncioTestCase):
    """Tests for get_token() method."""

    async def test_returns_cached_token_when_valid(self) -> None:
        """Test returns cached token without refreshing when still valid."""
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")
        manager._access_token = "cached_token"
        manager._expires_at = time.time() + 3600

        with patch.object(manager, "refresh_token") as mock_refresh:
            token = await manager.get_token()

        self.assertEqual(token, "cached_token")
        mock_refresh.assert_not_called()

    async def test_returns_cached_token_after_lock_double_check(self) -> None:
        """Test returns cached token after lock when token became valid.

        This tests the double-check pattern where another coroutine may have
        refreshed the token while this one was waiting for the lock.
        """
        manager = AsyncOAuth2TokenManager("id", "secret", "2.2")

        # Initially no token, but we'll set it after first is_token_valid check
        call_count = 0

        def mock_is_token_valid() -> bool:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First check: no token
                return False
            # After lock: token is now valid (set by another coroutine)
            manager._access_token = "token_from_other_coroutine"
            manager._expires_at = time.time() + 3600
            return True

        with patch.object(manager, "is_token_valid", side_effect=mock_is_token_valid):
            with patch.object(manager, "refresh_token") as mock_refresh:
                token = await manager.get_token()

        self.assertEqual(token, "token_from_other_coroutine")
        mock_refresh.assert_not_called()

    @patch("amazon_creatorsapi.core.async_auth.httpx.AsyncClient")
    async def test_refreshes_token_when_expired(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test refreshes token when expired."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_token",
            "expires_in": 3600,
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        manager = AsyncOAuth2TokenManager("test_id", "test_secret", "2.2")

        token = await manager.get_token()

        self.assertEqual(token, "new_token")
        self.assertEqual(manager._access_token, "new_token")
        self.assertIsNotNone(manager._expires_at)


class TestAsyncOAuth2TokenManagerRefreshToken(unittest.IsolatedAsyncioTestCase):
    """Tests for refresh_token() method."""

    @patch("amazon_creatorsapi.core.async_auth.httpx.AsyncClient")
    async def test_successful_token_refresh(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test successful token refresh."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "fresh_token",
            "expires_in": 7200,
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        manager = AsyncOAuth2TokenManager("test_id", "test_secret", "2.2")
        current_time = time.time()

        token = await manager.refresh_token()

        self.assertEqual(token, "fresh_token")
        self.assertEqual(manager._access_token, "fresh_token")
        expected_expiration = current_time + 7200 - TOKEN_EXPIRATION_BUFFER
        self.assertIsNotNone(manager._expires_at)
        assert manager._expires_at is not None  # for mypy
        self.assertAlmostEqual(
            manager._expires_at,
            expected_expiration,
            delta=2,  # Allow 2 second tolerance
        )

        # Verify correct request was made
        call_args = mock_client.post.call_args
        self.assertIn(GRANT_TYPE, str(call_args))
        self.assertIn(SCOPE, str(call_args))

    @patch("amazon_creatorsapi.core.async_auth.httpx.AsyncClient")
    async def test_raises_error_on_non_200_response(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test raises AuthenticationError on non-200 response."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        manager = AsyncOAuth2TokenManager("test_id", "test_secret", "2.2")

        with self.assertRaises(AuthenticationError) as context:
            await manager.refresh_token()

        self.assertIn("401", str(context.exception))

    @patch("amazon_creatorsapi.core.async_auth.httpx.AsyncClient")
    async def test_raises_error_when_no_access_token_in_response(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test raises AuthenticationError when response has no access_token."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": "invalid_scope"}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        manager = AsyncOAuth2TokenManager("test_id", "test_secret", "2.2")

        with self.assertRaises(AuthenticationError) as context:
            await manager.refresh_token()

        self.assertIn("No access token", str(context.exception))

    @patch("amazon_creatorsapi.core.async_auth.httpx.AsyncClient")
    async def test_raises_error_on_request_error(
        self,
        mock_async_client_class: MagicMock,
    ) -> None:
        """Test raises AuthenticationError on httpx.RequestError."""

        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.RequestError("Connection failed")
        mock_client.__aenter__.return_value = mock_client
        mock_async_client_class.return_value = mock_client

        manager = AsyncOAuth2TokenManager("test_id", "test_secret", "2.2")

        with self.assertRaises(AuthenticationError) as context:
            await manager.refresh_token()

        self.assertIn("token request failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
