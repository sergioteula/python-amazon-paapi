Amazon Product Advertising API 5.0 wrapper for Python
=======================================================
A simple Python wrapper for the last version of the Amazon Product Advertising API. This module allows to get product information from Amazon using the official API in an easier way.

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-2.x%20%7C%203.x-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-amazon-paapi/issues)
[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)


Features
--------

* Object oriented interface for simple usage.
* Get information about a product through its ASIN or URL.
* Get multiple products at once.
* Configurable throttling to avoid requests exceptions.
* Support for all available countries.
* Reorganized product information [structure](https://github.com/sergioteula/python-amazon-paapi/blob/master/PRODUCT.md) for simple use.
* Ask for new features through the [issues](https://github.com/sergioteula/python-amazon-paapi/issues) section.

Installation
-------------

You can install or upgrade the module with:

    pip install python-amazon-paapi --upgrade

Usage guide
-----------
Basic usage:

    from amazon.paapi import AmazonAPI
    amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
    product = amazon.get_product('B01N5IB20Q')
    print(product.title)

Get multiple product information:

    product = amazon.get_product('B01N5IB20Q,B01F9G43WU')
    print(product[0].images.large)
    print(product[1].prices.price.value)

Use URL insted of ASIN:

    product = amazon.get_product('https://www.amazon.com/dp/B01N5IB20Q')

Get the ASIN from a URL:

    from amazon.paapi import get_asin
    asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')

Changelog
-------------
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
