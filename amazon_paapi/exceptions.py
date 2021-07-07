"""Custom exceptions module"""


class AmazonException(Exception):
    """Common base class for all Amazon API exceptions."""
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return '%s' % self.message


class InvalidArgumentException(AmazonException):
    """Raised when arguments are not correct."""
    pass


class AsinNotFoundException(AmazonException):
    """Raised if the ASIN for an item is not found."""
    pass

class ApiRequestException(AmazonException):
    """Raised if the request to Amazon API fails"""
    pass

class MalformedRequestException(AmazonException):
    """Raised if the request for Amazon API is not correctly formed"""
    pass

class ItemsNotFoudException(AmazonException):
    """Raised if no items are found"""
    pass
