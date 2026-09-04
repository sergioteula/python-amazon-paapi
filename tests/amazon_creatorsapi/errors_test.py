"""Tests that pin the hierarchy of the errors of the library.

The hierarchy is what keeps the code written for an older version working
when an error gets a more precise type, so every relation checked here is a
promise made to the users and not an implementation detail.
"""

from __future__ import annotations

import unittest

from amazon_creatorsapi.errors import (
    AccessDeniedError,
    AmazonCreatorsApiError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
)

ERRORS = [
    AccessDeniedError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
]


class TestErrorHierarchy(unittest.TestCase):
    """Tests for the relations between the errors of the library."""

    def test_every_error_shares_the_base(self) -> None:
        """Test that a single except catches anything raised by the library."""
        for error in ERRORS:
            with self.subTest(error=error.__name__):
                self.assertTrue(issubclass(error, AmazonCreatorsApiError))

    def test_failures_of_a_request_are_request_errors(self) -> None:
        """Test that the errors of a rejected request keep being caught.

        Authentication and access failures were reported as RequestError
        before they got their own type, so they stay under it.
        """
        self.assertTrue(issubclass(AuthenticationError, RequestError))
        self.assertTrue(issubclass(AccessDeniedError, RequestError))

    def test_an_invalid_argument_is_a_value_error(self) -> None:
        """Test that an invalid value keeps being caught as a ValueError.

        The values rejected by the API constraints raised the ValidationError
        of pydantic, and an unsupported version raised a plain ValueError,
        both of which are ValueError subclasses.
        """
        self.assertTrue(issubclass(InvalidArgumentError, ValueError))

    def test_a_missing_resource_is_not_a_missing_item(self) -> None:
        """Test that feeds and reports are told apart from items."""
        self.assertFalse(issubclass(ResourceNotFoundError, ItemsNotFoundError))
        self.assertFalse(issubclass(ItemsNotFoundError, ResourceNotFoundError))


if __name__ == "__main__":
    unittest.main()
