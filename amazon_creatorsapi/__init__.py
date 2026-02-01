"""Amazon Creators API wrapper for Python.

A Python wrapper for the Amazon Creators API.
"""

from importlib.util import find_spec

__author__ = "Sergio Abad"
__all__ = ["AmazonCreatorsApi", "Country", "models"]

from . import models
from .api import AmazonCreatorsApi
from .core import Country

# Async support (requires 'async' extra: pip install python-amazon-paapi[async])
if find_spec("httpx") is not None:
    from .async_api import AsyncAmazonCreatorsApi

    __all__ += ["AsyncAmazonCreatorsApi"]
