"""Unit tests for the shared OAuth2 settings."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.oauth import (
    COGNITO_FLOW,
    COGNITO_SCOPE,
    LWA_FLOW,
    LWA_SCOPE,
    VERSION_ENDPOINTS,
    get_auth_endpoint,
    get_flow,
    get_scope,
    is_lwa,
)


class TestGetFlow(unittest.TestCase):
    """Tests for get_flow function."""

    def test_flow_of_the_known_families(self) -> None:
        """Test that the flow is taken from the major number of a version."""
        self.assertEqual(get_flow("2.4"), COGNITO_FLOW)
        self.assertEqual(get_flow("3.4"), LWA_FLOW)

    def test_flow_of_an_unknown_family(self) -> None:
        """Test that a family out of the known ones has no flow."""
        self.assertIsNone(get_flow("4.1"))
        self.assertIsNone(get_flow("not a version"))


class TestIsLwa(unittest.TestCase):
    """Tests for is_lwa function."""

    def test_lwa_versions(self) -> None:
        """Test that the 3.x versions authenticate with LWA."""
        for version in ("3.1", "3.2", "3.3"):
            self.assertTrue(is_lwa(version))

    def test_cognito_versions(self) -> None:
        """Test that the 2.x versions authenticate with Cognito."""
        for version in ("2.1", "2.2", "2.3"):
            self.assertFalse(is_lwa(version))


class TestGetScope(unittest.TestCase):
    """Tests for get_scope function."""

    def test_scope_of_every_version(self) -> None:
        """Test that every version asks for the scope of its flow."""
        self.assertEqual(get_scope("3.1"), LWA_SCOPE)
        self.assertEqual(get_scope("2.2"), COGNITO_SCOPE)


class TestGetAuthEndpoint(unittest.TestCase):
    """Tests for get_auth_endpoint function."""

    def test_endpoint_of_every_version(self) -> None:
        """Test that every supported version resolves to its endpoint."""
        for version, endpoint in VERSION_ENDPOINTS.items():
            self.assertEqual(get_auth_endpoint(version), endpoint)

    def test_custom_endpoint_wins(self) -> None:
        """Test that the endpoint given by the user is the one used."""
        self.assertEqual(
            get_auth_endpoint("2.2", "https://example.test/token"),
            "https://example.test/token",
        )

    def test_custom_endpoint_accepts_a_new_version_of_a_known_family(self) -> None:
        """Test that a custom endpoint accepts a version out of the list."""
        self.assertEqual(
            get_auth_endpoint("3.4", "https://example.test/token"),
            "https://example.test/token",
        )

    def test_custom_endpoint_is_stripped(self) -> None:
        """Test that the endpoint given by the user is used without spaces."""
        self.assertEqual(
            get_auth_endpoint("2.2", "  https://example.test/token\n"),
            "https://example.test/token",
        )

    def test_custom_endpoint_does_not_accept_an_unknown_family(self) -> None:
        """Test that a family with an unknown auth flow is always rejected."""
        with self.assertRaises(ValueError) as context:
            get_auth_endpoint("4.0", "https://example.test/token")

        self.assertIn("Unsupported version: 4.0", str(context.exception))
        self.assertIn("2.x, 3.x", str(context.exception))

    def test_blank_endpoint_is_ignored(self) -> None:
        """Test that a blank endpoint falls back to the one of the version."""
        self.assertEqual(get_auth_endpoint("2.2", "   "), VERSION_ENDPOINTS["2.2"])

    def test_unsupported_version_is_rejected(self) -> None:
        """Test that an unknown version without an endpoint is rejected."""
        with self.assertRaises(ValueError) as context:
            get_auth_endpoint("4.0")

        self.assertIn("Unsupported version: 4.0", str(context.exception))

    def test_error_of_a_known_family_points_to_the_custom_endpoint(self) -> None:
        """Test that the error of a new version explains how to use it."""
        with self.assertRaises(ValueError) as context:
            get_auth_endpoint("3.4")

        self.assertIn("Unsupported version: 3.4", str(context.exception))
        self.assertIn("auth_endpoint", str(context.exception))
