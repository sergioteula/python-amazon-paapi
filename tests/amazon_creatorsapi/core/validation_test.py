"""Unit tests for the validation utilities."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.validation import build_request, validate_timeout
from amazon_creatorsapi.errors import InvalidArgumentError
from creatorsapi_python_sdk.models.get_items_request_content import (
    GetItemsRequestContent,
)
from creatorsapi_python_sdk.models.search_items_request_content import (
    SearchItemsRequestContent,
)


class TestBuildRequest(unittest.TestCase):
    """Tests for build_request function."""

    def test_builds_the_request(self) -> None:
        """Test that a valid request is built with its values."""
        request = build_request(
            GetItemsRequestContent,
            partnerTag="test-tag",
            itemIds=["B0DLFMFBJW"],
        )
        self.assertEqual(request.partner_tag, "test-tag")
        self.assertEqual(request.item_ids, ["B0DLFMFBJW"])

    def test_invalid_value_raises_library_error(self) -> None:
        """Test that a rejected value raises an invalid argument error."""
        with self.assertRaises(InvalidArgumentError) as context:
            build_request(
                SearchItemsRequestContent,
                partnerTag="test-tag",
                keywords="laptop",
                minReviewsRating=5,
            )
        self.assertIn("minReviewsRating", str(context.exception))


class TestValidateTimeout(unittest.TestCase):
    """Tests for validate_timeout function."""

    def test_none_is_allowed(self) -> None:
        """Test that None disables the timeout."""
        self.assertIsNone(validate_timeout(None))

    def test_returns_a_float(self) -> None:
        """Test that the timeout is returned as a float."""
        self.assertEqual(validate_timeout(5), 5.0)

    def test_zero_is_rejected(self) -> None:
        """Test that a timeout of zero is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_timeout(0)
