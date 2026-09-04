"""Tests that pin the bundled SDK to the version rules of the library."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from amazon_creatorsapi.core.oauth import (
    VERSION_ENDPOINTS,
    build_authorization_header,
    get_scope,
    is_lwa,
)
from creatorsapi_python_sdk.api_client import ApiClient
from creatorsapi_python_sdk.auth.oauth2_config import OAuth2Config
from creatorsapi_python_sdk.configuration import Configuration

# Versions probed to find out which ones the bundled SDK knows, so a bump that
# adds one is noticed instead of leaving it unsupported by the library
CANDIDATE_VERSIONS = [
    f"{major}.{minor}" for major in range(1, 6) for minor in range(10)
]


def build_sdk_config(version: str) -> OAuth2Config:
    """Build the configuration that the SDK uses for a version."""
    return OAuth2Config("test_id", "test_secret", version, None)


class TestBundledSdkParity(unittest.TestCase):
    """Tests for the version rules duplicated in the bundled SDK.

    The library resolves the endpoint and the flow of a version on its own,
    so the copies of those rules in the bundled SDK are never used. They are
    checked here because the SDK is bumped from time to time, and a change in
    its rules that goes unnoticed would leave both halves disagreeing.
    """

    def request_header_of(self, version: str) -> str:
        """Return the Authorization header that the SDK sends for a version."""
        client = ApiClient(
            configuration=Configuration(),
            credential_id="test_id",
            credential_secret="test_secret",
            version=version,
            auth_endpoint="https://example.test/token",
        )
        client._token_manager = MagicMock()
        client._token_manager.get_token.return_value = "test_token"
        client.rest_client = MagicMock()

        client.call_api("POST", "https://example.test/catalog/v1/getItems")

        headers = client.rest_client.request.call_args.kwargs["headers"]
        return str(headers["Authorization"])

    def test_the_sdk_knows_the_same_versions(self) -> None:
        """Test that the SDK does not know a version out of the list."""
        known = set()

        for version in CANDIDATE_VERSIONS:
            try:
                build_sdk_config(version)
            except ValueError:
                continue
            known.add(version)

        self.assertEqual(known, set(VERSION_ENDPOINTS))

    def test_the_endpoint_of_every_version_matches(self) -> None:
        """Test that both halves send the token request to the same URL."""
        for version, endpoint in VERSION_ENDPOINTS.items():
            self.assertEqual(build_sdk_config(version).get_cognito_endpoint(), endpoint)

    def test_the_flow_of_every_version_matches(self) -> None:
        """Test that both halves authenticate a version the same way."""
        for version in VERSION_ENDPOINTS:
            config = build_sdk_config(version)
            self.assertEqual(config.is_lwa(), is_lwa(version))
            self.assertEqual(config.get_scope(), get_scope(version))

    def test_the_authorization_header_of_every_version_matches(self) -> None:
        """Test that both halves send the same Authorization header."""
        for version in VERSION_ENDPOINTS:
            self.assertEqual(
                self.request_header_of(version),
                build_authorization_header(version, "test_token"),
            )
