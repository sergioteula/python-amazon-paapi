"""Tests that pin the signatures of the public methods of both clients.

The position of an argument is part of the API: inserting one in the middle
silently binds the values of a caller that does not use keywords to the wrong
parameter. A new argument therefore goes at the end, and preferably as
keyword only, which is what these tests check.
"""

from __future__ import annotations

import inspect
import unittest
from typing import Callable

from amazon_creatorsapi import AmazonCreatorsApi
from amazon_creatorsapi.aio import AsyncAmazonCreatorsApi

# Positional arguments of every public method, in the order they are accepted
POSITIONAL_ARGUMENTS = {
    "__init__": [
        "credential_id",
        "credential_secret",
        "version",
        "tag",
        "country",
        "marketplace",
        "throttling",
        "timeout",
        "retries",
        "host",
        "auth_endpoint",
    ],
    "get_items": [
        "items",
        "condition",
        "currency_of_preference",
        "languages_of_preference",
        "resources",
    ],
    "search_items": [
        "keywords",
        "actor",
        "artist",
        "author",
        "brand",
        "title",
        "browse_node_id",
        "search_index",
        "item_count",
        "item_page",
        "condition",
        "currency_of_preference",
        "delivery_flags",
        "languages_of_preference",
        "max_price",
        "min_price",
        "min_saving_percent",
        "min_reviews_rating",
        "sort_by",
        "resources",
    ],
    "get_variations": [
        "asin",
        "variation_count",
        "variation_page",
        "condition",
        "currency_of_preference",
        "languages_of_preference",
        "resources",
    ],
    "get_browse_nodes": [
        "browse_node_ids",
        "languages_of_preference",
        "resources",
    ],
    "list_feeds": [],
    "get_feed": ["feed_name", "feed_type"],
    "list_reports": [],
    "get_report": ["filename", "report_type"],
}

# Arguments that can only be given by name, added after the ones above
KEYWORD_ONLY_ARGUMENTS = {
    "get_items": ["include_unavailable"],
    "search_items": ["availability"],
}

CLIENTS = [AmazonCreatorsApi, AsyncAmazonCreatorsApi]


def get_arguments(method: Callable[..., object], kind: object) -> list[str]:
    """Return the names of the arguments of a method for a kind of parameter."""
    parameters = inspect.signature(method).parameters.values()
    return [
        parameter.name
        for parameter in parameters
        if parameter.kind == kind and parameter.name != "self"
    ]


class TestClientSignatures(unittest.TestCase):
    """Tests for the arguments accepted by the methods of both clients."""

    def test_positional_arguments(self) -> None:
        """Test that the positional arguments keep their name and their order."""
        for client in CLIENTS:
            for name, expected in POSITIONAL_ARGUMENTS.items():
                with self.subTest(client=client.__name__, method=name):
                    arguments = get_arguments(
                        getattr(client, name),
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                    self.assertEqual(arguments, expected)

    def test_keyword_only_arguments(self) -> None:
        """Test that the arguments given by name are the expected ones."""
        for client in CLIENTS:
            for name in POSITIONAL_ARGUMENTS:
                with self.subTest(client=client.__name__, method=name):
                    arguments = get_arguments(
                        getattr(client, name),
                        inspect.Parameter.KEYWORD_ONLY,
                    )
                    self.assertEqual(arguments, KEYWORD_ONLY_ARGUMENTS.get(name, []))


if __name__ == "__main__":
    unittest.main()
