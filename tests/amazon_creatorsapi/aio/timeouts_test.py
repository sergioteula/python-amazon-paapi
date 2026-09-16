"""Unit tests for the conversion of the timeouts into httpx timeouts."""

from __future__ import annotations

import unittest

import httpx

from amazon_creatorsapi.aio.timeouts import build_httpx_timeout


class TestBuildHttpxTimeout(unittest.TestCase):
    """Tests for build_httpx_timeout function."""

    def test_none_waits_indefinitely(self) -> None:
        """Test that None is passed through as no timeout."""
        self.assertIsNone(build_httpx_timeout(None))

    def test_seconds_are_passed_through(self) -> None:
        """Test that a single value reaches httpx as it did before."""
        self.assertEqual(build_httpx_timeout(5), 5)

    def test_pair_bounds_every_leg(self) -> None:
        """Test that a pair bounds each leg, leaving none of them unbounded.

        Handed a pair of its own, httpx reads it as the first two of
        (connect, read, write, pool) and leaves the write and the pool legs
        unbounded, dropping a timeout that the single value form applies. The
        read value covers them instead.
        """
        timeout = build_httpx_timeout((1, 5))

        self.assertEqual(timeout, httpx.Timeout(connect=1, read=5, write=5, pool=5))
        self.assertNotEqual(
            timeout,
            httpx.Timeout(connect=1, read=5, write=None, pool=None),
        )
