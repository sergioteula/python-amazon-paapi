"""Constants for the Amazon Creators API."""

DEFAULT_HOST = "https://creatorsapi.amazon"
DEFAULT_THROTTLING = 1
DEFAULT_TIMEOUT = 30.0

# Maximum amount of item identifiers accepted in a single request
MAX_ITEMS_PER_REQUEST = 10

# HTTP status codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
