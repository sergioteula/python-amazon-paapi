"""Constants for the Amazon Creators API."""

from __future__ import annotations

from typing import Union

TimeoutValue = Union[float, "tuple[float, float]"]
"""Seconds for the whole request, or ``(connect, read)`` seconds per leg.

The pair matters for a host that resolves to several addresses: the connect
leg is spent once per address, so a single value generous enough to read a
slow response is also spent on every address that fails to answer.
"""

DEFAULT_HOST = "https://creatorsapi.amazon"
DEFAULT_THROTTLING = 1
# Connect and read seconds, rather than one value covering both. The connect
# leg is spent once per address the host resolves to, so a single value
# generous enough to read a slow response is also spent on every address that
# fails to answer: at 30 seconds, a host resolving to four addresses takes two
# minutes to give up. The two add up to the 30 seconds this has always
# documented, and a connection that takes longer than five seconds to
# establish is not one that a longer wait rescues.
DEFAULT_TIMEOUT = (5.0, 25.0)

# Maximum amount of item identifiers accepted in a single request
MAX_ITEMS_PER_REQUEST = 10

# HTTP status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
