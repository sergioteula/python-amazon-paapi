"""Conversion of the timeout values into the ones httpx understands.

It lives here rather than next to the values themselves because httpx is an
optional dependency, and the synchronous client must keep importing without
it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amazon_creatorsapi.core.constants import TimeoutValue

try:
    import httpx
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc


def build_httpx_timeout(
    timeout: TimeoutValue | None,
) -> float | httpx.Timeout | None:
    """Return the timeout to hand to httpx for a value the clients accept.

    A pair is the only value httpx needs help with. Everything else is passed
    through as it is, so httpx keeps reading it exactly as it did before pairs
    were accepted.

    Args:
        timeout: Seconds for the whole request, ``(connect, read)`` seconds
            per leg, or None to wait indefinitely.

    Returns:
        The seconds, the httpx timeout built from the pair, or None to wait
        indefinitely.

    """
    if not isinstance(timeout, tuple):
        return timeout
    connect, read = timeout
    # httpx reads a pair as (connect, read, write, pool) and leaves the two it
    # does not find unbounded, which would drop a timeout that the single
    # value form applies. The read value covers them instead.
    return httpx.Timeout(connect=connect, read=read, write=read, pool=read)
