"""Containers for API results that also carry partial errors."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

    from creatorsapi_python_sdk.models.error_data import ErrorData

ResultT = TypeVar("ResultT")


class ResultList(list[ResultT]):
    """List of results that also exposes the partial errors sent by Amazon.

    A request for several identifiers can succeed while only returning some of
    them, listing the reason for the missing ones as partial errors. This list
    behaves like any other list and keeps those errors available.

    Example:
        >>> items = api.get_items(["B0DLFMFBJW", "0000000000"])
        >>> for error in items.errors:
        ...     print(error.code, error.message)

    """

    def __init__(
        self,
        results: Iterable[ResultT] = (),
        errors: Iterable[ErrorData] | None = None,
    ) -> None:
        """Initialize the list with its results and their partial errors."""
        super().__init__(results)
        self.errors: list[ErrorData] = list(errors) if errors else []
