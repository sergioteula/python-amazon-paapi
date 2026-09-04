"""Custom exceptions for the Amazon Creators API."""


class AmazonCreatorsApiError(Exception):
    """Base exception for Amazon Creators API."""


class InvalidArgumentError(AmazonCreatorsApiError, ValueError):
    """Raised when an invalid argument is provided.

    Also a ValueError, so the code written against the errors that pydantic
    and the version check raised before keeps catching it.
    """


class RequestError(AmazonCreatorsApiError):
    """Raised when the API request fails."""


class ItemsNotFoundError(AmazonCreatorsApiError):
    """Raised when no items are found."""


class TooManyRequestsError(AmazonCreatorsApiError):
    """Raised when the rate limit is exceeded."""


class AssociateValidationError(AmazonCreatorsApiError):
    """Raised when associate credentials are invalid."""


class AuthenticationError(RequestError):
    """Raised when OAuth2 authentication fails.

    A request that fails to authenticate is a failed request, so it is also a
    RequestError.
    """


class AccessDeniedError(RequestError):
    """Raised when the credentials cannot perform the requested operation.

    A request rejected for lack of access is a failed request, so it is also
    a RequestError.
    """


class ResourceNotFoundError(AmazonCreatorsApiError):
    """Raised when the requested feed or report does not exist."""


__all__ = [
    "AccessDeniedError",
    "AmazonCreatorsApiError",
    "AssociateValidationError",
    "AuthenticationError",
    "InvalidArgumentError",
    "ItemsNotFoundError",
    "RequestError",
    "ResourceNotFoundError",
    "TooManyRequestsError",
]
