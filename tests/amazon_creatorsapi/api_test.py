"""Unit tests for AmazonCreatorsApi class."""

from __future__ import annotations

import time
import unittest
from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import MagicMock

from amazon_creatorsapi import AmazonCreatorsApi
from amazon_creatorsapi.errors import InvalidArgumentError

if TYPE_CHECKING:
    from amazon_creatorsapi.helpers import CountryCode


class TestAmazonCreatorsApi(unittest.TestCase):
    """Tests for AmazonCreatorsApi class."""

    def setUp(self) -> None:
        self.credential_id = "test_credential_id"
        self.credential_secret = "test_credential_secret"  # noqa: S105
        self.version = "2.2"
        self.tag = "test-tag"
        self.country: CountryCode = "ES"

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_with_country(self, mock_client: MagicMock) -> None:
        """Test initialization with country code."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
        )
        self.assertEqual(api.marketplace, "www.amazon.es")
        self.assertEqual(api.tag, self.tag)
        mock_client.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_with_marketplace(self, _mock_client: MagicMock) -> None:
        """Test initialization with direct marketplace URL."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            marketplace="www.amazon.co.uk",
        )
        self.assertEqual(api.marketplace, "www.amazon.co.uk")

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_init_marketplace_overrides_country(self, _mock_client: MagicMock) -> None:
        """Test that marketplace parameter overrides country."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country="ES",
            marketplace="www.amazon.com",
        )
        self.assertEqual(api.marketplace, "www.amazon.com")

    def test_init_invalid_country(self) -> None:
        """Test initialization with invalid country code raises exception."""
        with self.assertRaises(InvalidArgumentError):
            AmazonCreatorsApi(
                credential_id=self.credential_id,
                credential_secret=self.credential_secret,
                version=self.version,
                tag=self.tag,
                country="INVALID",  # type: ignore[arg-type]
            )

    def test_init_no_country_or_marketplace(self) -> None:
        """Test initialization without country or marketplace raises exception."""
        with self.assertRaises(InvalidArgumentError):
            AmazonCreatorsApi(
                credential_id=self.credential_id,
                credential_secret=self.credential_secret,
                version=self.version,
                tag=self.tag,
            )

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_throttling_disabled(self, _mock_client: MagicMock) -> None:
        """Test that API call is not delayed when throttling is 0."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
        )
        start_time = time.time()
        api._throttle()
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 0.1)

    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_throttling_sleeps(self, _mock_client: MagicMock) -> None:
        """Test that API call is delayed according to throttling setting."""
        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0.2,
        )
        api._last_query_time = time.time()
        start_time = time.time()
        api._throttle()
        elapsed_time = time.time() - start_time
        self.assertGreater(elapsed_time, 0.1)

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_get_items(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test get_items method returns items."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.items_result.items = [MagicMock()]
        mock_api.get_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
        )
        result = api.get_items(["B0DLFMFBJW"])
        self.assertIsInstance(result, list)
        mock_api.get_items.assert_called_once()

    @mock.patch("amazon_creatorsapi.api.DefaultApi")
    @mock.patch("amazon_creatorsapi.api.ApiClient")
    def test_search_items(
        self,
        _mock_client_class: MagicMock,
        mock_api_class: MagicMock,
    ) -> None:
        """Test search_items method returns results."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_response = MagicMock()
        mock_response.search_result = MagicMock()
        mock_api.search_items.return_value = mock_response

        api = AmazonCreatorsApi(
            credential_id=self.credential_id,
            credential_secret=self.credential_secret,
            version=self.version,
            tag=self.tag,
            country=self.country,
            throttling=0,
        )
        result = api.search_items(keywords="laptop")
        self.assertIsNotNone(result)
        mock_api.search_items.assert_called_once()
