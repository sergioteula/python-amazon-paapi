"""Custom exceptions module."""


class AmazonCreatorsApiError(Exception):
    """Base exception for Amazon Creators API."""


class InvalidArgumentError(AmazonCreatorsApiError):
    """Raised when an invalid argument is provided."""


class MalformedRequestError(AmazonCreatorsApiError):
    """Raised when the request is malformed."""


class RequestError(AmazonCreatorsApiError):
    """Raised when the API request fails."""


class ItemsNotFoundError(AmazonCreatorsApiError):
    """Raised when no items are found."""


class TooManyRequestsError(AmazonCreatorsApiError):
    """Raised when the rate limit is exceeded."""


class AssociateValidationError(AmazonCreatorsApiError):
    """Raised when associate credentials are invalid."""
