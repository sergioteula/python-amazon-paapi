"""Async OAuth2 token manager for Amazon Creators API.

Handles OAuth2 token acquisition, caching, and automatic refresh using async HTTP.
"""

from __future__ import annotations

import asyncio
import time

from amazon_creatorsapi.errors import AuthenticationError

try:
    import httpx
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc


# OAuth2 constants
SCOPE = "creatorsapi/default"
GRANT_TYPE = "client_credentials"

# Token expiration buffer in seconds (refresh 30s before actual expiration)
TOKEN_EXPIRATION_BUFFER = 30

# Version to auth endpoint mapping
VERSION_ENDPOINTS = {
    "2.1": "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token",
    "2.2": "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token",
    "2.3": "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token",
}


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

    """

    def __init__(
        self,
        credential_id: str,
        credential_secret: str,
        version: str,
        auth_endpoint: str | None = None,
    ) -> None:
        """Initialize the async OAuth2 token manager."""
        self._credential_id = credential_id
        self._credential_secret = credential_secret
        self._version = version
        self._auth_endpoint = self._determine_auth_endpoint(version, auth_endpoint)

        self._access_token: str | None = None
        self._expires_at: float | None = None
        self._lock = asyncio.Lock()

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
            ValueError: If version is not supported and no custom endpoint provided.

        """
        if auth_endpoint and auth_endpoint.strip():
            return auth_endpoint

        if version not in VERSION_ENDPOINTS:
            supported = ", ".join(VERSION_ENDPOINTS.keys())
            msg = f"Unsupported version: {version}. Supported versions are: {supported}"
            raise ValueError(msg)

        return VERSION_ENDPOINTS[version]

    async def get_token(self) -> str:
        """Get a valid OAuth2 access token, refreshing if necessary.

        Returns:
            A valid access token.

        Raises:
            AuthenticationError: If token acquisition fails.

        """
        if self.is_token_valid():
            # Token is cached and still valid, guaranteed to be str here
            assert self._access_token is not None  # noqa: S101
            return self._access_token

        # Need to refresh - use lock to prevent concurrent refreshes
        async with self._lock:
            # Double-check after acquiring lock
            if self.is_token_valid():
                assert self._access_token is not None  # noqa: S101
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
            "scope": SCOPE,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._auth_endpoint,
                    data=request_data,
                    headers=headers,
                )

            if response.status_code != 200:  # noqa: PLR2004
                self.clear_token()
                msg = (
                    f"OAuth2 token request failed with status {response.status_code}: "
                    f"{response.text}"
                )
                raise AuthenticationError(msg)

            data = response.json()

            if "access_token" not in data:
                self.clear_token()
                msg = "No access token received from OAuth2 endpoint"
                raise AuthenticationError(msg)

            self._access_token = data["access_token"]
            # Set expiration time with buffer to avoid edge cases
            expires_in = data.get("expires_in", 3600)
            self._expires_at = time.time() + expires_in - TOKEN_EXPIRATION_BUFFER

        except httpx.RequestError as exc:
            self.clear_token()
            msg = f"OAuth2 token request failed: {exc}"
            raise AuthenticationError(msg) from exc

        return self._access_token

    def clear_token(self) -> None:
        """Clear the cached token, forcing a refresh on the next get_token() call."""
        self._access_token = None
        self._expires_at = None
