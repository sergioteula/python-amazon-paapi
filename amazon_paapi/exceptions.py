"""Custom exceptions class."""


class AmazonException(Exception):
    """Custom exceptions class for Amazon Product Advertising API."""
    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        return '%s: %s' % (self.status, self.reason)
