"""Async OAuth2 token manager for Amazon Creators API.

Handles OAuth2 token acquisition, caching, and automatic refresh using async HTTP.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from amazon_creatorsapi.core.constants import DEFAULT_TIMEOUT, HTTP_OK
from amazon_creatorsapi.core.oauth import (
    COGNITO_SCOPE,
    DEFAULT_EXPIRATION,
    GRANT_TYPE,
    LWA_SCOPE,
    TOKEN_EXPIRATION_BUFFER,
    VERSION_ENDPOINTS,
    get_auth_endpoint,
    get_scope,
    is_lwa,
)
from amazon_creatorsapi.errors import AuthenticationError

try:
    import httpx
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc


# Backward-compatible alias for existing v2.x users.
SCOPE = COGNITO_SCOPE

__all__ = [
    "COGNITO_SCOPE",
    "GRANT_TYPE",
    "LWA_SCOPE",
    "SCOPE",
    "TOKEN_EXPIRATION_BUFFER",
    "VERSION_ENDPOINTS",
    "AsyncOAuth2TokenManager",
]


class AsyncOAuth2TokenManager:
    """Async OAuth2 token manager with caching for Amazon Creators API.

    Manages the OAuth2 token lifecycle including:
    - Token acquisition via client credentials grant
    - Token caching with automatic expiration tracking
    - Automatic token refresh when expired
    - Async-safe token refresh with locking

    Args:
        credential_id: OAuth2 credential ID.
        credential_secret: OAuth2 credential secret.
        version: API version (determines auth endpoint).
        auth_endpoint: Optional custom auth endpoint URL.
        timeout: Token request timeout in seconds, or None to wait
            indefinitely. Defaults to 30 seconds.

    """

    def __init__(
        self,
        credential_id: str,
        credential_secret: str,
        version: str,
        auth_endpoint: str | None = None,
        timeout: float | None = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the async OAuth2 token manager."""
        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self._auth_endpoint = self._determine_auth_endpoint(version, auth_endpoint)
        self._timeout = timeout

        self._access_token: str | None = None
        self._expires_at: float | None = None
        self._lock: asyncio.Lock | None = None

    def _determine_auth_endpoint(
        self,
        version: str,
        auth_endpoint: str | None,
    ) -> str:
        """Determine the OAuth2 token endpoint based on version or custom endpoint.

        Args:
            version: API version.
            auth_endpoint: Optional custom auth endpoint.

        Returns:
            The OAuth2 token endpoint URL.

        Raises:
            InvalidArgumentError: If version is not supported and no custom
                endpoint provided.

        """
        return get_auth_endpoint(version, auth_endpoint)

    def is_lwa(self) -> bool:
        """Return whether this token manager uses the LWA auth flow."""
        return is_lwa(self._version)

    def get_scope(self) -> str:
        """Return the version-appropriate OAuth2 scope."""
        return get_scope(self._version)

    @property
    def lock(self) -> asyncio.Lock:
        """Lazy initialization of the asyncio.Lock.

        The lock must be created lazily to support Python 3.9, where
        asyncio.Lock() requires an event loop to exist. By creating it
        on first access (which happens in an async context), we ensure
        an event loop is available.

        Returns:
            The asyncio.Lock instance.

        """
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    async def get_token(self) -> str:
        """Get a valid OAuth2 access token, refreshing if necessary.

        Returns:
            A valid access token.

        Raises:
            AuthenticationError: If token acquisition fails.

        """
        if self.is_token_valid():
            # Token is cached and still valid, guaranteed to be str here
            if self._access_token is None:
                msg = "Token should be valid at this point"
                raise AuthenticationError(msg)
            return self._access_token

        # Need to refresh - use lock to prevent concurrent refreshes
        async with self.lock:
            # Double-check after acquiring lock
            if self.is_token_valid():
                if self._access_token is None:
                    msg = "Token should be valid at this point"
                    raise AuthenticationError(msg)
                return self._access_token
            return await self.refresh_token()

    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired.

        Returns:
            True if the token is valid, False otherwise.

        """
        return (
            self._access_token is not None
            and self._expires_at is not None
            and time.time() < self._expires_at
        )

    async def refresh_token(self) -> str:
        """Refresh the OAuth2 access token using client credentials grant.

        Returns:
            The new access token.

        Raises:
            AuthenticationError: If token refresh fails.

        """
        request_data = {
            "grant_type": GRANT_TYPE,
            "client_id": self._credential_id,
            "client_secret": self._credential_secret,
            "scope": self.get_scope(),
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                if self.is_lwa():
                    response = await client.post(
                        self._auth_endpoint,
                        json=request_data,
                        headers={"Content-Type": "application/json"},
                    )
                else:
                    response = await client.post(
                        self._auth_endpoint,
                        data=request_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                    )

            if response.status_code != HTTP_OK:
                self.clear_token()
                msg = (
                    f"OAuth2 token request failed with status {response.status_code}: "
                    f"{response.text}"
                )
                raise AuthenticationError(msg)

            data = self._parse_token_response(response)

            if "access_token" not in data:
                self.clear_token()
                msg = "No access token received from OAuth2 endpoint"
                raise AuthenticationError(msg)

            self._access_token = data["access_token"]
            # Set expiration time with buffer to avoid edge cases
            expires_in = data.get("expires_in", DEFAULT_EXPIRATION)
            self._expires_at = time.time() + expires_in - TOKEN_EXPIRATION_BUFFER

        except httpx.RequestError as exc:
            self.clear_token()
            msg = f"OAuth2 token request failed: {exc}"
            raise AuthenticationError(msg) from exc

        # At this point, self._access_token is guaranteed to be a string
        if self._access_token is None:
            msg = "Token should be set at this point"
            raise AuthenticationError(msg)
        return self._access_token

    def _parse_token_response(self, response: httpx.Response) -> dict[str, Any]:
        """Parse the token response as JSON.

        Args:
            response: Response from the auth endpoint.

        Returns:
            The parsed response body.

        Raises:
            AuthenticationError: If the response is not valid JSON.

        """
        try:
            data: dict[str, Any] = response.json()
        except ValueError as error:
            self.clear_token()
            msg = f"Failed to parse OAuth2 token response: {error}"
            raise AuthenticationError(msg) from error
        return data

    def clear_token(self) -> None:
        """Clear the cached token, forcing a refresh on the next get_token() call."""
        self._access_token = None
        self._expires_at = None
