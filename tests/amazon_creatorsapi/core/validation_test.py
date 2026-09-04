"""Unit tests for the validation utilities."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.validation import (
    build_request,
    validate_retries,
    validate_search_criteria,
    validate_throttling,
    validate_timeout,
)
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

    def test_not_a_number_is_rejected(self) -> None:
        """Test that a value that is not a number is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_timeout("slow")  # type: ignore[arg-type]


class TestValidateRetries(unittest.TestCase):
    """Tests for validate_retries function."""

    def test_returns_the_amount(self) -> None:
        """Test that a valid amount of retries is returned."""
        self.assertEqual(validate_retries(2), 2)

    def test_zero_disables_retries(self) -> None:
        """Test that no retries is a valid value."""
        self.assertEqual(validate_retries(0), 0)

    def test_negative_is_rejected(self) -> None:
        """Test that a negative amount of retries is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_retries(-1)

    def test_not_a_number_is_rejected(self) -> None:
        """Test that a value that is not a whole number is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_retries("many")  # type: ignore[arg-type]


class TestValidateThrottling(unittest.TestCase):
    """Tests for validate_throttling function."""

    def test_accepts_a_wait_time(self) -> None:
        """Test that a wait time is returned as a float."""
        self.assertEqual(validate_throttling(2), 2.0)

    def test_accepts_no_wait_time(self) -> None:
        """Test that no wait between calls is accepted."""
        self.assertEqual(validate_throttling(0), 0.0)

    def test_negative_is_rejected(self) -> None:
        """Test that a negative wait time is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_throttling(-1)

    def test_not_a_number_is_rejected(self) -> None:
        """Test that a value that is not a number is rejected."""
        with self.assertRaises(InvalidArgumentError):
            validate_throttling("fast")  # type: ignore[arg-type]


class TestValidateSearchCriteria(unittest.TestCase):
    """Tests for validate_search_criteria function."""

    def test_accepts_one_criterion(self) -> None:
        """Test that a single criterion is enough to search."""
        validate_search_criteria(keywords="laptop", brand=None)

    def test_rejects_a_search_without_criteria(self) -> None:
        """Test that a search without criteria is rejected."""
        with self.assertRaises(InvalidArgumentError) as context:
            validate_search_criteria(keywords=None, brand=None)

        self.assertIn("keywords, brand", str(context.exception))
