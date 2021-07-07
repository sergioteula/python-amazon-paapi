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
