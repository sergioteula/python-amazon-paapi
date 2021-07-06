"""Custom exception class."""


class AmazonException(Exception):
    """Custom exception class for Amazon Product Advertising API."""
    def __init__(self, status=None, reason=None):
        self.status = status
        self.reason = reason

    def __str__(self):
        return '%s: %s' % (self.status, self.reason)
