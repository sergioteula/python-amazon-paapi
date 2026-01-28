"""Amazon Creators API wrapper for Python.

A Python wrapper for the Amazon Creators API.
"""

__author__ = "Sergio Abad"
__all__ = ["AmazonCreatorsApi", "get_asin"]

from .api import AmazonCreatorsApi
from .tools import get_asin
