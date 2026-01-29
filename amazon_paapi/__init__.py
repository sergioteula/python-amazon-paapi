"""Amazon Product Advertising API wrapper for Python.

DEPRECATED: This module is deprecated and will be removed in a future version.
Use `amazon_creatorsapi` instead.
"""

import warnings

warnings.warn(
    "The 'amazon_paapi' module is deprecated and will be removed in a future version. "
    "Please use 'amazon_creatorsapi' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__author__ = "Sergio Abad"
__all__ = ["AmazonApi", "get_asin"]

from .api import AmazonApi  # noqa: E402
from .tools import get_asin  # noqa: E402
