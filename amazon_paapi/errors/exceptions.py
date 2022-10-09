"""Custom exceptions module"""


class AmazonException(Exception):
    """Common base class for all Amazon API exceptions."""

    def __init__(self, reason: str):
        super().__init__()
        self.reason = reason

    def __str__(self) -> str:
        return self.reason


class InvalidArgumentException(AmazonException):
    """Raised when arguments are not correct."""


class AsinNotFoundException(AmazonException):
    """Raised if the ASIN for an item is not found."""


class ApiRequestException(AmazonException):
    """Raised if the request to Amazon API fails"""


class MalformedRequestException(AmazonException):
    """Raised if the request for Amazon API is not correctly formed"""


class ItemsNotFoundException(AmazonException):
    """Raised if no items are found"""


class TooManyRequestsException(AmazonException):
    """Raised when requests limit is reached"""


class InvalidPartnerTagException(AmazonException):
    """Raised if the partner tag is not present or invalid"""


class AssociateValidationException(AmazonException):
    """Raised when credentials are not valid for the selected country"""
