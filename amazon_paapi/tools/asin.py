"""Some useful tools."""

from ..errors import AsinNotFoundException
import re


def get_asin(text: str) -> str:
    """Returns the ASIN from a given text. Raises AsinNotFoundException on fail."""
    # Return if text is an ASIN
    if re.search(r'^[A-Z0-9]{10}$', text):
        return text

    # Extract ASIN from URL searching for alphanumeric and 10 digits
    asin = re.search(r'(dp|gp/product|gp/aw/d|dp/product)/([a-zA-Z0-9]{10})', text)
    if asin:
        return asin.group(2)
    else:
        raise AsinNotFoundException('Asin not found: ' + text)
