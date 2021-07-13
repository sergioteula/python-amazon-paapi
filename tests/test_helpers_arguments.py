from amazon_paapi.exceptions import AsinNotFoundException, InvalidArgumentException
from amazon_paapi.helpers.arguments import get_items_ids
import pytest


def test_get_items_ids():
    amazon_url = 'https://www.amazon.es/gp/product/B07PHPXHQS'
    assert get_items_ids('B01N5IB20Q') == ['B01N5IB20Q']
    assert get_items_ids('B01N5IB20Q,B01N5IB20Q,B01N5IB20Q') == ['B01N5IB20Q','B01N5IB20Q','B01N5IB20Q']
    assert get_items_ids(['B01N5IB20Q','B01N5IB20Q','B01N5IB20Q']) == ['B01N5IB20Q','B01N5IB20Q','B01N5IB20Q']
    assert get_items_ids(amazon_url) == ['B07PHPXHQS']
    assert get_items_ids([amazon_url,amazon_url]) == ['B07PHPXHQS', 'B07PHPXHQS']

    with pytest.raises(AsinNotFoundException):
        get_items_ids('https://www.amazon.es/gp/')
    with pytest.raises(InvalidArgumentException):
        get_items_ids(34)
