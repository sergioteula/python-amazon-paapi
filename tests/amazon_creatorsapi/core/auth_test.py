"""Unit tests for the OAuth2 token manager with timeout."""

from __future__ import annotations

import threading
import time
import unittest
from unittest import mock
from unittest.mock import MagicMock

import requests

from amazon_creatorsapi.core.auth import TimeoutOAuth2TokenManager
from amazon_creatorsapi.errors import AuthenticationError
from creatorsapi_python_sdk.auth.oauth2_config import OAuth2Config


class TestTimeoutOAuth2TokenManager(unittest.TestCase):
    """Tests for TimeoutOAuth2TokenManager class."""

    def setUp(self) -> None:
        self.config = OAuth2Config("test_id", "test_secret", "2.2", None)
        self.manager = TimeoutOAuth2TokenManager(self.config, timeout=7.0)

    def build_response(self, status_code: int = 200, **json_data: object) -> MagicMock:
        """Build a fake response for the auth endpoint."""
        response = MagicMock()
        response.status_code = status_code
        response.text = "response body"
        response.json.return_value = json_data or {
            "access_token": "test_token",
            "expires_in": 3600,
        }
        return response

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_token_request_uses_the_timeout(self, mock_post: MagicMock) -> None:
        """Test that the timeout is sent with the token request."""
        mock_post.return_value = self.build_response()

        token = self.manager.refresh_token()

        self.assertEqual(token, "test_token")
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 7.0)
        self.assertIn("data", mock_post.call_args.kwargs)

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_lwa_token_request_uses_json_body(self, mock_post: MagicMock) -> None:
        """Test that LWA versions send the credentials as JSON."""
        manager = TimeoutOAuth2TokenManager(
            OAuth2Config("test_id", "test_secret", "3.1", None),
            timeout=None,
        )
        mock_post.return_value = self.build_response()

        manager.refresh_token()

        self.assertIn("json", mock_post.call_args.kwargs)
        self.assertIsNone(mock_post.call_args.kwargs["timeout"])

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_token_is_cached(self, mock_post: MagicMock) -> None:
        """Test that a valid token is reused instead of requested again."""
        mock_post.return_value = self.build_response()

        self.assertEqual(self.manager.get_token(), "test_token")
        self.assertEqual(self.manager.get_token(), "test_token")
        mock_post.assert_called_once()

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_error_status_raises_authentication_error(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Test that a failed token request raises an authentication error."""
        mock_post.return_value = self.build_response(status_code=401)

        with self.assertRaises(AuthenticationError) as context:
            self.manager.refresh_token()

        self.assertIn("401", str(context.exception))
        self.assertIsNone(self.manager.access_token)

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_missing_token_raises_authentication_error(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Test that a response without token raises an authentication error."""
        mock_post.return_value = self.build_response(token_type="Bearer")

        with self.assertRaises(AuthenticationError) as context:
            self.manager.refresh_token()

        self.assertIn("No access token", str(context.exception))

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_request_error_raises_authentication_error(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Test that a timed out request raises an authentication error."""
        mock_post.side_effect = requests.Timeout("timed out")

        with self.assertRaises(AuthenticationError) as context:
            self.manager.refresh_token()

        self.assertIn("token request failed", str(context.exception))

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_invalid_json_raises_authentication_error(
        self,
        mock_post: MagicMock,
    ) -> None:
        """Test that an unparseable response raises an authentication error."""
        response = self.build_response()
        response.json.side_effect = ValueError("no json")
        mock_post.return_value = response

        with self.assertRaises(AuthenticationError) as context:
            self.manager.refresh_token()

        self.assertIn("parse OAuth2 token response", str(context.exception))


class TestTimeoutOAuth2TokenManagerThreads(unittest.TestCase):
    """Tests for the token manager when it is shared by several threads."""

    @mock.patch("amazon_creatorsapi.core.auth.requests.post")
    def test_only_one_thread_requests_the_token(self, mock_post: MagicMock) -> None:
        """Test that threads asking at once share a single token request."""
        started = threading.Barrier(4)

        def build_token(*_args: object, **_kwargs: object) -> MagicMock:
            # The request takes long enough for the other threads to reach the
            # cache while it is still empty
            time.sleep(0.05)
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = {
                "access_token": "test_token",
                "expires_in": 3600,
            }
            return response

        mock_post.side_effect = build_token

        manager = TimeoutOAuth2TokenManager(
            OAuth2Config("test_id", "test_secret", "2.2", None),
            timeout=7.0,
        )
        tokens: list[str] = []

        def get_token() -> None:
            started.wait()
            tokens.append(manager.get_token())

        threads = [threading.Thread(target=get_token) for _ in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(tokens, ["test_token"] * 4)
        self.assertEqual(mock_post.call_count, 1)
