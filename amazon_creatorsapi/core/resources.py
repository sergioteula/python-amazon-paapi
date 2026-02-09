"""Resource utilities for the Amazon Creators API."""

from __future__ import annotations

from enum import Enum
from typing import TypeVar

# TypeVar for generic resource handling
ResourceT = TypeVar("ResourceT", bound=Enum)


def get_all_resources(resource_class: type[ResourceT]) -> list[ResourceT]:
    """Extract all resource values from a resource enum class.

    Args:
        resource_class: Enum class containing resource definitions.

    Returns:
        List of all enum members from the resource class.

    """
    return list(resource_class)
