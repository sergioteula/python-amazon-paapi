"""Unit tests for the retry utilities."""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

from amazon_creatorsapi.core.retry import (
    MAX_BACKOFF,
    get_retry_after,
    get_retry_delay,
    is_retryable,
)


class TestIsRetryable(unittest.TestCase):
    """Tests for is_retryable function."""

    def test_retryable_statuses(self) -> None:
        """Test that throttling and server errors are retried."""
        for status_code in (429, 500, 502, 503, 504):
            self.assertTrue(is_retryable(status_code))

    def test_not_retryable_statuses(self) -> None:
        """Test that client errors and successes are not retried."""
        for status_code in (200, 400, 401, 403, 404, None):
            self.assertFalse(is_retryable(status_code))


class TestGetRetryAfter(unittest.TestCase):
    """Tests for get_retry_after function."""

    def test_reads_the_header(self) -> None:
        """Test that the header value is read as seconds."""
        self.assertEqual(get_retry_after({"Retry-After": "5"}), 5.0)

    def test_header_is_case_insensitive(self) -> None:
        """Test that the header is found whatever its case is."""
        self.assertEqual(get_retry_after({"retry-after": "2"}), 2.0)

    def test_missing_header(self) -> None:
        """Test that no header means no requested wait."""
        self.assertIsNone(get_retry_after({}))
        self.assertIsNone(get_retry_after(None))
        self.assertIsNone(get_retry_after({"Content-Type": "application/json"}))

    def test_reads_a_date_header(self) -> None:
        """Test that a header holding a date is read as the seconds left."""
        date = datetime.now(timezone.utc) + timedelta(seconds=120)
        seconds = get_retry_after({"Retry-After": format_datetime(date, usegmt=True)})

        self.assertIsNotNone(seconds)
        assert seconds is not None
        self.assertAlmostEqual(seconds, 120, delta=5)

    def test_date_header_in_the_past(self) -> None:
        """Test that a date already past asks for no wait at all."""
        date = datetime.now(timezone.utc) - timedelta(seconds=120)

        self.assertEqual(
            get_retry_after({"Retry-After": format_datetime(date, usegmt=True)}),
            0.0,
        )

    def test_date_header_without_timezone(self) -> None:
        """Test that a date without timezone is read as UTC."""
        date = datetime.now(timezone.utc) + timedelta(seconds=120)
        header = date.strftime("%a, %d %b %Y %H:%M:%S")
        seconds = get_retry_after({"Retry-After": header})

        self.assertIsNotNone(seconds)
        assert seconds is not None
        self.assertAlmostEqual(seconds, 120, delta=5)

    def test_invalid_header_is_ignored(self) -> None:
        """Test that a header holding neither seconds nor a date is ignored."""
        self.assertIsNone(get_retry_after({"Retry-After": "soon"}))


class TestGetRetryDelay(unittest.TestCase):
    """Tests for get_retry_delay function."""

    def test_delay_grows_with_every_attempt(self) -> None:
        """Test that the wait time doubles on every attempt."""
        delays = [get_retry_delay(attempt) for attempt in range(3)]
        self.assertEqual(delays, [1.0, 2.0, 4.0])

    def test_delay_is_capped(self) -> None:
        """Test that the wait time never goes over the maximum."""
        self.assertEqual(get_retry_delay(20), MAX_BACKOFF)

    def test_retry_after_takes_precedence(self) -> None:
        """Test that the wait requested by Amazon is honoured."""
        self.assertEqual(get_retry_delay(0, {"Retry-After": "7"}), 7.0)

    def test_retry_after_is_capped(self) -> None:
        """Test that the requested wait never goes over the maximum."""
        self.assertEqual(get_retry_delay(0, {"Retry-After": "600"}), MAX_BACKOFF)
