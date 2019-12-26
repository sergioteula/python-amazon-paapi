Amazon Product Advertising API V5 wrapper for Python
=======================================================
A simple Python wrapper for the Amazon Product Advertising API version 5.

Features
--------

* Object oriented interface for simple usage
* Get information about a product through its ASIN
* More coming in the future

Installation
-------------

     pip install python-amazon-paapi5

Usage
-----

     from amazon.paapi import AmazonAPI
     amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)
     product = amazon.get_product(asin)


License
-------

Copyright &copy; 2019 Sergio Abad
