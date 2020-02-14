Amazon Product Advertising API 5.0 wrapper for Python
=======================================================
A simple Python wrapper for the last version of the Amazon Product Advertising API.

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi5?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi5/)
[![Python](https://img.shields.io/badge/Python-2.x%20%7C%203.x-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0-%23e83633)](https://github.com/sergioteula/python-amazon-paapi5/blob/master/LICENSE)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-amazon-paapi5/issues)
[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)


Features
--------

* Object oriented interface for simple usage
* Get information about a product through its ASIN
* More coming in the future

Installation
-------------

You can install or upgrade the module with:

     pip install python-amazon-paapi5 --upgrade

Changelog
-------------

Release 0.1.1

     - Added currency support for prices.

Usage
-----

     from amazon.paapi import AmazonAPI
     amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
     product = amazon.get_product(asin)


License
-------

This software is licensed under the GNU General Public License v3.0 that you can check [here](https://github.com/sergioteula/python-amazon-paapi5/blob/master/LICENSE).
