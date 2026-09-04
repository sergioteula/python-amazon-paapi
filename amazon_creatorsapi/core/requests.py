"""Utilities to build the body of a request for the API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import BaseModel


def get_request_body(request: BaseModel) -> dict[str, Any]:
    """Return the body to send to the API for a request model.

    Args:
        request: Request model from the SDK.

    Returns:
        The values of the request using the names of the API, without the
        ones that were not provided.

    """
    body: dict[str, Any] = request.model_dump(
        by_alias=True,
        exclude_none=True,
        mode="json",
    )
    return body
