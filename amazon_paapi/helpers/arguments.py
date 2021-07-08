"""Module with helper functions for managing arguments."""


from ..tools import get_asin
from ..errors import InvalidArgumentException
from typing import Union


def get_items_ids(items: Union[str, list[str]]) -> list[str]:
    if not isinstance(items, str) and not isinstance(items, list):
        raise InvalidArgumentException('Invalid items argument, it should be a string or list of strings')

    if isinstance(items, str):
        items_ids = items.split(',')
        return [get_asin(x.strip()) for x in items_ids]

    else:
        return [get_asin(x.strip()) for x in items]
