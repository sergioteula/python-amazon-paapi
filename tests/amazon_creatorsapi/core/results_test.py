"""Unit tests for the result containers."""

from __future__ import annotations

import unittest

from amazon_creatorsapi.core.results import ResultList
from creatorsapi_python_sdk.models.error_data import ErrorData


class TestResultList(unittest.TestCase):
    """Tests for ResultList class."""

    def setUp(self) -> None:
        self.error = ErrorData(code="ItemNotFound", message="Item not found")

    def test_behaves_like_a_list(self) -> None:
        """Test that the container is a regular list of results."""
        result = ResultList([1, 2, 3])
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(len(result), 3)

    def test_keeps_errors(self) -> None:
        """Test that partial errors are available in the errors attribute."""
        result = ResultList([1], errors=[self.error])
        self.assertEqual(result.errors, [self.error])

    def test_empty_errors_by_default(self) -> None:
        """Test that the errors attribute defaults to an empty list."""
        self.assertEqual(ResultList().errors, [])
