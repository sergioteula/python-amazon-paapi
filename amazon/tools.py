"""Some useful tools."""

import re


def get_asin(url: str):
    """Find the ASIN from a given URL.

    Args:
        url (str): The URL containing the product ASIN.

    Returns:
        str: Product ASIN. None if ASIN not found.
    """
    # Return if url parameter already is the ASIN
    if re.search(r'^[A-Z0-9]{10}$', url):
        return url
    # Extract ASIN from URL searching for alphanumeric and 10 digits
    have_asin = re.search(r'(dp|gp/product|gp/aw/d|dp/product)/([a-zA-Z0-9]{10})', url)
    return have_asin.group(2) if have_asin else None


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
