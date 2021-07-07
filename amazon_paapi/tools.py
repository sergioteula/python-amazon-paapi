"""Some useful tools."""

import re


def get_asin(text: str) -> str:
    """Returns the ASIN from a given text. Raises AsinNotFoundException on fail."""
    # Return if url parameter already is the ASIN
    if re.search(r'^[A-Z0-9]{10}$', text):
        return text
    # Extract ASIN from URL searching for alphanumeric and 10 digits
    have_asin = re.search(r'(dp|gp/product|gp/aw/d|dp/product)/([a-zA-Z0-9]{10})', text)
    return have_asin.group(2) if have_asin else None


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
