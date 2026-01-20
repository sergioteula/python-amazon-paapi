"""Custom exceptions for the Amazon Creators API."""

from .exceptions import (
    AmazonCreatorsApiError,
    AssociateValidationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    MalformedRequestError,
    RequestError,
    TooManyRequestsError,
)

__all__ = [
    "AmazonCreatorsApiError",
    "AssociateValidationError",
    "InvalidArgumentError",
    "ItemsNotFoundError",
    "MalformedRequestError",
    "RequestError",
    "TooManyRequestsError",
]
