Amazon Product Advertising API 5.0 wrapper for Python
=======================================================
A simple Python wrapper for the [last version of the Amazon Product Advertising API](https://webservices.amazon.com/paapi5/documentation/quick-start/using-sdk.html). This module allows to get product information from Amazon using the official API in an easier way.

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-2.x%20%7C%203.x-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-amazon-paapi/issues)
[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)


Features
--------

* Object oriented interface for simple usage.
* Get information about a product through its ASIN or URL.
* Get item variations or search for products on Amazon.
* Get browse nodes information.
* Get multiple results at once without the 10 items limitation from Amazon.
* Configurable throttling to avoid requests exceptions.
* Built-in serializer for Django REST framework.
* Support for [all available countries](https://github.com/sergioteula/python-amazon-paapi/blob/master/amazon/paapi.py#L31).
* Reorganized product information [structure](https://github.com/sergioteula/python-amazon-paapi/blob/master/PRODUCT.md) for simple use.
* Ask for new features through the [issues](https://github.com/sergioteula/python-amazon-paapi/issues) section.
* Join our [Telegram group](https://t.me/PythonAmazonPAAPI) for support or development.

Installation
-------------

You can install or upgrade the module with:

    pip install python-amazon-paapi --upgrade

If you get `ModuleNotFoundError`, try installing this:

    pip install amightygirl.paapi5-python-sdk

Usage guide
-----------
**Basic usage:**

````python
from amazon.paapi import AmazonAPI
amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
product = amazon.get_product('B01N5IB20Q')
print(product.title)
````

**Get multiple product information:**

````python
product = amazon.get_products('B01N5IB20Q,B01F9G43WU')
print(product[0].images.large)
print(product[1].prices.price.value)
````

**Use URL insted of ASIN:**

````python
product = amazon.get_product('https://www.amazon.com/dp/B01N5IB20Q')
````

**Get product variations:**

````python
product = amazon.get_variations('B01N5IB20Q')
print(product[0].title)
````

**Search product:**

````python
product = amazon.search_products(item_count=25, keywords='speaker')
print(product[14].url)
````

**Get browse node information:**

````python
node = amazon.get_browsenodes(browse_nodes=browsenodes_list)
````

**Get the ASIN from a URL:**

````python
from amazon.tools import get_asin
asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')
````

**Throttling:**

Throttling value must be `greater than 0` or `False` to disable it. This value throttles requests to a maximum of one request every `1 / value` seconds. Note that this value is a per-worker throttling, so applications with multiple workers may make more requests per second. Throttling value is [set by default](https://github.com/sergioteula/python-amazon-paapi/blob/master/amazon/paapi.py#L36) to `0.8` or one request every 1.25 seconds.

````python
amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY, throttling=0.5)  # Max one request every two seconds
amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY, throttling=False)  # Unlimited requests per second
````

**Serializer for Django:**

We provide a serializer for Django REST framework, which speeds up your API
implementation.

````python
from amazon.serializers import AmazonProductSerializer
from rest_framework import serializers

serialized_product = AmazonProductSerializer(product)
serialized_product.data
````

If you want to serialize a list of products:

````python
serialized_products = AmazonProductSerializer(products, many=True)
serialized_products.data
````

For more information on how to work with serializers, check the documentation for
[Django REST framework](https://www.django-rest-framework.org/api-guide/serializers/).


Changelog
-------------
    Version 3.3.2
        - Allow sending several products ids on get_product.
        - Updated get_asin for new URL format.
        - Added NL region support.
        - Removed type hints.

    Version 3.3.1
        - Allow searching by browse_node or search_index alone.
        - Added license files for Amazon SDK.
        - Solved bugs and typos.

    Version 3.3.0
        - Added serializer class for Django REST framework.
        - Solved bugs and typos.

    Version 3.2.0
        - Added new method for getting browse nodes information.
        - Removed the 10 pages limit on search_products and get_variations methods.
        - Solved unnecessary API call on search_products and get_variations methods.

    Version 3.1.0
        - Added paapi5-python-sdk and removed amightygirl.paapi5-python-sdk.
        - Improved throttling and now possible to disable it.
        - Bug fixes.

    Version 3.0.2
        - Changed to MIT License.

    Version 3.0.1
        - Solved import bug.

    Version 3.0.0
        - Added search_products and get_variations methods.
        - Removed Amazon API requests limit for all methods.
        - Created AmazonException for better exception handling.
        - Added asynchronous requests compatibility.
        - Added parent_ASIN to product instance.
        - Cleaned code for more consistent style.
        - Updated docstrings for all methods.
        - Updated project structure.

    Version 2.1.1
        - Added get_product for single requests.

    Version 2.1.0
        - Changed get_product method name to get_products.
        - Removed Amazon 10 products limitation.
        - Added type hints.
        - Solved bug with images exception.
        - Updated documentation.

    Version 2.0.1
        - Improved exception handling.

    Version 2.0.0
        - New structure for product info, adding all available information from the API.
        - Added raw_data with the information unparsed from the API.
        - Removed Amazon API version from package name to avoid changes in the future.

    Version 1.0.0
        - Added support for getting multiple product information.
        - Added compatibiliy with Amazon URL search.
        - New function for getting the ASIN for a given URL.
        - Removed Amazon SDK and added as a requirement.
        - Updated docstrings.
        - Updated README with changelog, more examples and badges.

    Version 0.1.1
        - Added currency support for prices.

    Version 0.1.0
        -First release.

License
-------------
Copyright © 2020 Sergio Abad. See [license](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE) for details.
