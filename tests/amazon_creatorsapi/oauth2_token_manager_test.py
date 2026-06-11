"""Unit tests for OAuth2TokenManager proxy support."""

from __future__ import annotations

import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from creatorsapi_python_sdk.auth.oauth2_config import OAuth2Config
from creatorsapi_python_sdk.auth.oauth2_token_manager import OAuth2TokenManager


def _make_config(version: str = "2.2") -> OAuth2Config:
    return OAuth2Config(
        credential_id="test_id",
        credential_secret="test_secret",
        version=version,
        auth_endpoint=None,
    )


def _mock_token_response() -> MagicMock:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"access_token": "tok123", "expires_in": 3600}
    return resp


class TestOAuth2TokenManagerProxy(unittest.TestCase):
    """Tests that OAuth2TokenManager routes token refresh through the proxy."""

    @patch("creatorsapi_python_sdk.auth.oauth2_token_manager.requests.Session")
    def test_refresh_token_sets_proxies_on_session(self, mock_session_cls: MagicMock) -> None:
        """When proxies are provided, Session.proxies.update is called with them."""
        proxy_url = "http://user:pass@proxy.example.com:3128"
        proxies = {"http": proxy_url, "https": proxy_url}

        mock_session = MagicMock()
        mock_session.post.return_value = _mock_token_response()
        mock_session_cls.return_value = mock_session

        manager = OAuth2TokenManager(_make_config(), proxies=proxies)
        manager.refresh_token()

        mock_session.proxies.update.assert_called_once_with(proxies)

    @patch("creatorsapi_python_sdk.auth.oauth2_token_manager.requests.Session")
    def test_refresh_token_no_proxy_skips_proxies_update(self, mock_session_cls: MagicMock) -> None:
        """When no proxy is configured, Session.proxies.update is not called."""
        mock_session = MagicMock()
        mock_session.post.return_value = _mock_token_response()
        mock_session_cls.return_value = mock_session

        manager = OAuth2TokenManager(_make_config())
        manager.refresh_token()

        mock_session.proxies.update.assert_not_called()

    @patch("creatorsapi_python_sdk.auth.oauth2_token_manager.requests.Session")
    def test_refresh_token_lwa_sets_proxies_on_session(self, mock_session_cls: MagicMock) -> None:
        """Proxy is also applied for LWA (v3.x) token refresh."""
        proxy_url = "http://proxy.example.com:3128"
        proxies = {"http": proxy_url, "https": proxy_url}

        mock_session = MagicMock()
        mock_session.post.return_value = _mock_token_response()
        mock_session_cls.return_value = mock_session

        manager = OAuth2TokenManager(_make_config(version="3.1"), proxies=proxies)
        manager.refresh_token()

        mock_session.proxies.update.assert_called_once_with(proxies)
