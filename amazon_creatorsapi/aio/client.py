"""Async HTTP client for Amazon Creators API.

Provides an async HTTP client using httpx for making API requests.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.metadata import version
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

if TYPE_CHECKING:
    from types import TracebackType

try:
    import httpx
except ImportError as exc:  # pragma: no cover
    msg = (
        "httpx is required for async support. "
        "Install it with: pip install python-amazon-paapi[async]"
    )
    raise ImportError(msg) from exc


DEFAULT_HOST = "https://creatorsapi.amazon"
DEFAULT_TIMEOUT = 30.0
VERSION = version("python-amazon-paapi")
USER_AGENT = f"python-amazon-paapi/{VERSION} (async)"


@dataclass
class AsyncHttpResponse:
    """Response from an async HTTP request."""

    status_code: int
    headers: dict[str, str]
    body: bytes
    text: str

    def json(self) -> dict[str, Any]:
        """Parse response body as JSON."""
        result: dict[str, Any] = json.loads(self.text)
        return result


class AsyncHttpClient:
    """Async HTTP client for Amazon Creators API.

    This client can be used in two ways:

    1. Without context manager (creates a new connection per request):
        >>> client = AsyncHttpClient()
        >>> response = await client.post("/path", headers, body)

    2. With context manager (reuses connection for multiple requests):
        >>> async with AsyncHttpClient() as client:
        ...     response = await client.post("/path", headers, body)

    The context manager approach is more efficient when making multiple
    requests in quick succession due to HTTP connection pooling.

    Args:
        host: Base URL for API requests. Defaults to Amazon Creators API.
        timeout: Request timeout in seconds. Defaults to 30.

    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the async HTTP client."""
        self._host = host
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None
        self._owns_client = False

    async def __aenter__(self) -> Self:
        """Enter async context manager, creating a persistent client."""
        self._client = httpx.AsyncClient(
            base_url=self._host,
            timeout=self._timeout,
            headers={"User-Agent": USER_AGENT},
        )
        self._owns_client = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager, closing the client."""
        if self._client is not None and self._owns_client:
            await self._client.aclose()
            self._client = None
            self._owns_client = False

    async def post(
        self,
        path: str,
        headers: dict[str, str],
        body: dict[str, Any],
    ) -> AsyncHttpResponse:
        """Make a POST request to the API.

        Args:
            path: API endpoint path (e.g., "/catalog/v1/getItems").
            headers: Request headers.
            body: Request body as a dictionary.

        Returns:
            AsyncHttpResponse with status, headers, and body.

        """
        all_headers = {"User-Agent": USER_AGENT, **headers}

        if self._client is not None:
            # Use persistent client (context manager mode)
            response = await self._client.post(
                path,
                headers=all_headers,
                json=body,
            )
        else:
            # Create a new client for this request (standalone mode)
            async with httpx.AsyncClient(
                base_url=self._host,
                timeout=self._timeout,
            ) as client:
                response = await client.post(
                    path,
                    headers=all_headers,
                    json=body,
                )

        return AsyncHttpResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=response.content,
            text=response.text,
        )
