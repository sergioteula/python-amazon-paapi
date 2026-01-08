"""Module with helper functions for making generators."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def get_list_chunks(
    full_list: list[str], chunk_size: int
) -> Generator[list[str], None, None]:
    """Yield successive chunks from List."""
    for i in range(0, len(full_list), chunk_size):
        yield full_list[i : i + chunk_size]
