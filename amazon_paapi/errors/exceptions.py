"""Custom exceptions module"""


class AmazonError(Exception):
    """Common base class for all Amazon API exceptions."""

    def __init__(self, reason: str):
        super().__init__()
        self.reason = reason

    def __str__(self) -> str:
        return self.reason


class AsinNotFound(AmazonError):
    """Raised if the ASIN for an item is not found."""


class AssociateValidationError(AmazonError):
    """Raised when credentials are not valid for the selected country."""


class InvalidArgument(AmazonError):
    """Raised when arguments are not correct."""


class InvalidPartnerTag(AmazonError):
    """Raised if the partner tag is not present or invalid."""


class ItemsNotFound(AmazonError):
    """Raised if no items are found."""


class MalformedRequest(AmazonError):
    """Raised if the request for Amazon API is not correctly formed."""


class RequestError(AmazonError):
    """Raised if the request to Amazon API fails."""


class TooManyRequests(AmazonError):
    """Raised when requests limit is reached."""
