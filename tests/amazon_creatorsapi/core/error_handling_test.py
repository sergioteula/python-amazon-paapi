"""Unit tests for the error handling utilities."""

from __future__ import annotations

import json
import unittest

from amazon_creatorsapi.core.error_handling import (
    get_request_id,
    handle_api_error,
    parse_error_body,
)
from amazon_creatorsapi.errors import (
    AccessDeniedError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
)


class TestParseErrorBody(unittest.TestCase):
    """Tests for parse_error_body function."""

    def test_parses_a_json_object(self) -> None:
        """Test that a JSON object is returned as a dictionary."""
        self.assertEqual(parse_error_body('{"reason": "Other"}'), {"reason": "Other"})

    def test_ignores_anything_else(self) -> None:
        """Test that a body that is not a JSON object is ignored."""
        self.assertEqual(parse_error_body("<html>error</html>"), {})
        self.assertEqual(parse_error_body("[1, 2]"), {})
        self.assertEqual(parse_error_body(""), {})


class TestHandleApiError(unittest.TestCase):
    """Tests for handle_api_error function."""

    def build_body(self, **data: object) -> str:
        """Build the body of an error response."""
        return json.dumps(data)

    def test_validation_error(self) -> None:
        """Test that a rejected request raises an invalid argument error."""
        body = self.build_body(
            type="ValidationException",
            message="Request is not valid",
            reason="FieldValidationFailed",
            fieldList=[{"name": "itemIds", "message": "must not be empty"}],
        )

        with self.assertRaises(InvalidArgumentError) as context:
            handle_api_error(400, body)

        message = str(context.exception)
        self.assertIn("FieldValidationFailed", message)
        self.assertIn("itemIds: must not be empty", message)

    def test_invalid_associate(self) -> None:
        """Test that an invalid associate raises its own error."""
        body = self.build_body(message="Invalid associate", reason="InvalidAssociate")

        with self.assertRaises(AssociateValidationError):
            handle_api_error(400, body)

    def test_invalid_associate_without_json_body(self) -> None:
        """Test that the reason is found even when the body is not JSON."""
        with self.assertRaises(AssociateValidationError):
            handle_api_error(400, "InvalidAssociate for this marketplace")

    def test_invalid_partner_tag(self) -> None:
        """Test that an invalid partner tag raises an invalid argument error."""
        body = self.build_body(message="Invalid tag", reason="InvalidPartnerTag")

        with self.assertRaises(InvalidArgumentError) as context:
            handle_api_error(400, body)

        self.assertIn("InvalidPartnerTag", str(context.exception))

    def test_unauthorized(self) -> None:
        """Test that an expired token raises an authentication error."""
        body = self.build_body(message="Token expired", reason="TokenExpired")

        with self.assertRaises(AuthenticationError) as context:
            handle_api_error(401, body)

        self.assertIn("TokenExpired", str(context.exception))

    def test_access_denied(self) -> None:
        """Test that a forbidden request raises an access denied error."""
        body = self.build_body(message="Not eligible", reason="AssociateNotEligible")

        with self.assertRaises(AccessDeniedError) as context:
            handle_api_error(403, body)

        self.assertIn("AssociateNotEligible", str(context.exception))

    def test_not_found_defaults_to_items(self) -> None:
        """Test that a missing resource raises the items error by default."""
        with self.assertRaises(ItemsNotFoundError):
            handle_api_error(404, "")

    def test_not_found_can_be_customized(self) -> None:
        """Test that a missing feed or report raises its own error."""
        body = self.build_body(
            message="Not found",
            resourceId="report.csv",
            resourceType="Report",
        )

        with self.assertRaises(ResourceNotFoundError) as context:
            handle_api_error(404, body, ResourceNotFoundError)

        self.assertIn("report.csv", str(context.exception))

    def test_throttled(self) -> None:
        """Test that a throttled request raises a too many requests error."""
        with self.assertRaises(TooManyRequestsError):
            handle_api_error(429, self.build_body(message="Slow down"))

    def test_server_error(self) -> None:
        """Test that an unexpected status raises a request error."""
        with self.assertRaises(RequestError) as context:
            handle_api_error(500, self.build_body(message="Internal error"))

        self.assertIn("500", str(context.exception))
        self.assertIn("Internal error", str(context.exception))

    def test_body_without_details(self) -> None:
        """Test that an unparseable body is kept in the message."""
        with self.assertRaises(RequestError) as context:
            handle_api_error(502, "<html>Bad gateway</html>")

        self.assertIn("Bad gateway", str(context.exception))


class TestHandleApiErrorReason(unittest.TestCase):
    """Tests for the reason reported when the response has no body."""

    def test_reason_is_reported(self) -> None:
        """Test that the reason is kept when the response has no body."""
        with self.assertRaises(RequestError) as context:
            handle_api_error(0, "", reason="SSL error: certificate verify failed")

        self.assertIn("certificate verify failed", str(context.exception))

    def test_body_wins_over_the_reason(self) -> None:
        """Test that the body of the response is preferred to the reason."""
        with self.assertRaises(RequestError) as context:
            handle_api_error(
                500,
                '{"message": "Internal failure"}',
                reason="Internal Server Error",
            )

        self.assertIn("Internal failure", str(context.exception))
        self.assertNotIn("Internal Server Error", str(context.exception))


class TestGetRequestId(unittest.TestCase):
    """Tests for get_request_id function."""

    def test_reads_the_header(self) -> None:
        """Test that the identifier of the request is found."""
        self.assertEqual(get_request_id({"x-amzn-RequestId": "abc-123"}), "abc-123")

    def test_missing_header(self) -> None:
        """Test that a response without the header has no identifier."""
        self.assertIsNone(get_request_id({"Content-Type": "application/json"}))
        self.assertIsNone(get_request_id(None))

    def test_request_id_is_reported(self) -> None:
        """Test that the identifier is part of the message of the error."""
        with self.assertRaises(RequestError) as context:
            handle_api_error(500, "", headers={"x-amzn-requestid": "abc-123"})

        self.assertIn("abc-123", str(context.exception))
