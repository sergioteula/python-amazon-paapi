"""Async support for Amazon Creators API."""

try:
    import httpx  # noqa: F401
except ImportError as exc:
    msg = (
        "httpx is required for async support. "
        "Install with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc

from amazon_creatorsapi.aio.api import AsyncAmazonCreatorsApi

__all__ = ["AsyncAmazonCreatorsApi"]
