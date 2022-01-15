# Amazon Product Advertising API 5.0 wrapper for Python

A simple Python wrapper for the [last version of the Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/quick-start/using-sdk.html). This module allows interacting with Amazon using the official API in an easier way.

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python->3.6-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)
[![Codecov](https://img.shields.io/codecov/c/github/sergioteula/python-amazon-paapi?label=Coverage)](https://app.codecov.io/gh/sergioteula/python-amazon-paapi/)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-amazon-paapi/issues)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Installs)](https://pypi.org/project/python-amazon-paapi/)

> If you are still using the old version, go [here](https://github.com/sergioteula/python-amazon-paapi/blob/master/amazon/README.md) for documentation or check our
[migration guide](https://github.com/sergioteula/python-amazon-paapi/blob/master/docs/pages/migration-guide.md).

## Features

- Object oriented interface for simple usage.
- Get information about a product through its ASIN or URL.
- Get item variations or search for products on Amazon.
- Get browse nodes information.
- Get multiple results at once without the 10 items limitation from Amazon.
- Configurable throttling to avoid requests exceptions.
- Type hints to help you coding.
- Support for [all available countries](https://github.com/sergioteula/python-amazon-paapi/blob/956f639b2ab3eab3f61644ae2ca8ae6500881312/amazon_paapi/models/regions.py#L1).
- Ask for new features through the [issues](https://github.com/sergioteula/python-amazon-paapi/issues) section.
- Join our [Telegram group](https://t.me/PythonAmazonPAAPI) for support or development.
- Check the [documentation](https://python-amazon-paapi.readthedocs.io/en/latest/index.html) for reference.

## Installation

You can install or upgrade the module with:

    pip install python-amazon-paapi --upgrade

## Usage guide

**Basic usage:**

```python
from amazon_paapi import AmazonApi
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY)
item = amazon.get_items('B01N5IB20Q')[0]
print(item.item_info.title.display_value) # Item title
```

**Get multiple items information:**

```python
items = amazon.get_items(['B01N5IB20Q', 'B01F9G43WU'])
for item in items:
    print(item.images.primary.large.url) # Primary image url
    print(item.offers.listings[0].price.amount) # Current price
```

**Use URL insted of ASIN:**

```python
item = amazon.get_items('https://www.amazon.com/dp/B01N5IB20Q')
```

**Get item variations:**

```python
variations = amazon.get_variations('B01N5IB20Q')
for item in variations.items:
    print(item.detail_page_url) # Affiliate url
```

**Search items:**

```python
search_result = amazon.search_items(keywords='nintendo')
for item in search_result.items:
    print(item.item_info.product_info.color) # Item color
```

**Get browse node information:**

```python
browse_nodes = amazon.get_browse_nodes(['667049031', '599385031'])
for browse_node in browse_nodes:
    print(browse_node.display_name) # The name of the node
```

**Get the ASIN from URL:**

```python
from amazon_paapi import get_asin
asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')
```

**Throttling:**

Throttling value represents the wait time in seconds between API calls, being the default value 1 second. Use it to avoid reaching Amazon request limits.

```python
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=4)  # Makes 1 request every 4 seconds
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=0)  # No wait time between requests
```

## License

Copyright © 2021 Sergio Abad. See [license](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE) for details.
