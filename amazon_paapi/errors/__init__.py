"""Custom exceptions for the Amazon Product Advertising API."""

from .exceptions import (
    AmazonError,
    AsinNotFound,
    AssociateValidationError,
    InvalidArgument,
    InvalidPartnerTag,
    ItemsNotFound,
    MalformedRequest,
    RequestError,
    TooManyRequests,
)

__all__ = [
    "AmazonError",
    "AsinNotFound",
    "AssociateValidationError",
    "InvalidArgument",
    "InvalidPartnerTag",
    "ItemsNotFound",
    "MalformedRequest",
    "RequestError",
    "TooManyRequests",
]
