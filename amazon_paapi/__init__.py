"""Amazon Product Advertising API wrapper for Python."""

__author__ = "Sergio Abad"
__all__ = ["AmazonApi", "get_asin"]

from .api import AmazonApi
from .tools import get_asin
