"""Custom exceptions for the Amazon Creators API."""


class AmazonCreatorsApiError(Exception):
    """Base exception for Amazon Creators API."""


class InvalidArgumentError(AmazonCreatorsApiError):
    """Raised when an invalid argument is provided."""


class RequestError(AmazonCreatorsApiError):
    """Raised when the API request fails."""


class ItemsNotFoundError(AmazonCreatorsApiError):
    """Raised when no items are found."""


class TooManyRequestsError(AmazonCreatorsApiError):
    """Raised when the rate limit is exceeded."""


class AssociateValidationError(AmazonCreatorsApiError):
    """Raised when associate credentials are invalid."""


__all__ = [
    "AmazonCreatorsApiError",
    "AssociateValidationError",
    "InvalidArgumentError",
    "ItemsNotFoundError",
    "RequestError",
    "TooManyRequestsError",
]
