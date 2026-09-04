"""OAuth2 token manager that applies a timeout to the token requests."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, Any

import requests

from amazon_creatorsapi.core.constants import HTTP_OK
from amazon_creatorsapi.core.oauth import DEFAULT_EXPIRATION, TOKEN_EXPIRATION_BUFFER
from amazon_creatorsapi.errors import AuthenticationError
from creatorsapi_python_sdk.auth.oauth2_token_manager import OAuth2TokenManager

if TYPE_CHECKING:
    from creatorsapi_python_sdk.auth.oauth2_config import OAuth2Config


class TimeoutOAuth2TokenManager(OAuth2TokenManager):
    """Token manager that fails instead of waiting forever for a token.

    The token manager bundled with the SDK requests the token without any
    timeout, so an unresponsive auth endpoint blocks the call indefinitely
    even when a timeout is set for the API requests themselves. It also asks
    for a token without any lock, so every thread sharing a client requests
    its own token as soon as the cached one expires.

    Args:
        config: OAuth2 configuration with the credentials and the endpoint.
        timeout: Token request timeout in seconds, or None to wait
            indefinitely.

    """

    def __init__(self, config: OAuth2Config, timeout: float | None) -> None:
        """Initialize the token manager with its timeout."""
        super().__init__(config)
        self._timeout = timeout
        self._lock = threading.Lock()

    def get_token(self) -> str:
        """Return a valid token, asking for a new one only once at a time.

        Returns:
            A valid access token.

        Raises:
            AuthenticationError: If the token cannot be obtained.

        """
        if self.is_token_valid():
            return str(self.access_token)

        with self._lock:
            if self.is_token_valid():
                return str(self.access_token)
            return self.refresh_token()

    def refresh_token(self) -> str:
        """Refresh the OAuth2 access token using the client credentials grant.

        Returns:
            The new access token.

        Raises:
            AuthenticationError: If the token cannot be obtained.

        """
        response = self._request_token()

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

        self.access_token = data["access_token"]
        expires_in = data.get("expires_in", DEFAULT_EXPIRATION)
        self.expires_at = time.time() + expires_in - TOKEN_EXPIRATION_BUFFER

        return str(self.access_token)

    def _request_token(self) -> requests.Response:
        """Request a new token to the auth endpoint.

        Returns:
            The response from the auth endpoint.

        Raises:
            AuthenticationError: If the request cannot be completed.

        """
        request_data = {
            "grant_type": self.config.get_grant_type(),
            "client_id": self.config.get_credential_id(),
            "client_secret": self.config.get_credential_secret(),
            "scope": self.config.get_scope(),
        }
        endpoint = self.config.get_cognito_endpoint()

        try:
            if self.config.is_lwa():
                return requests.post(
                    endpoint,
                    json=request_data,
                    headers={"Content-Type": "application/json"},
                    timeout=self._timeout,
                )
            return requests.post(
                endpoint,
                data=request_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self._timeout,
            )
        except requests.RequestException as error:
            self.clear_token()
            msg = f"OAuth2 token request failed: {error}"
            raise AuthenticationError(msg) from error

    def _parse_token_response(self, response: requests.Response) -> dict[str, Any]:
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
