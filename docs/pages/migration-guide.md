# Migration guide

This guide explains how to proceed with the migration from version 3.x to version 4.x of your current code.
If you are still using the old version, it is highly recommended to update, since you wont get any future
updates nor new features.

## Version 4 changelog summary

- Added type hinting to help you code.
- Added compatibility with all arguments from the official API.
- Now the full information from the API is returned, instead of a trimmed version.
- Added custom exceptions to help with error handling.
- Added models for some attributes.
- Adjusted all methods and models to meet Amazon API standards.
- Changed module name from amazon to amazon_paapi to avoid module clashes.
- Compatibility with Python 3.6 or later.

## How to upgrade?

Upgrading to the last version of this module is as easy as running this pip command:

    pip install python-amazon-paapi --upgrade

## What should I change in my current code?

### Imports

First of all, you should change your import of the AmazonApi class:

```python
from amazon.paapi import AmazonApi  ->  from amazon_paapi import AmazonApi
from amazon.tools import get_asin   ->  from amazon_paapi import get_asin
```

### Methods

Some of the methods has been renamed and the parameters has changed to follow the official Amazon API standards.
So in order to adapt your code, you should first update your methods as follow:

```python
get_product()       ->  get_items()
get_products()      ->  get_items()
search_products()   ->  search_items()
get_browsenodes()   ->  get_browse_nodes()
```

As you can check, `get_product` has been deprecated and now `get_items` is also used for getting only one result.
So if you were using this method, you should keep in mind that the new method will return an array containing the
result. An easy way of handling this could be:

```python
result = get_product(asin) -> result = get_items(asin)[0]
```

Regarding parameters, you can check the [AmazonApi documentation](/amazon_paapi) for the complete reference.

### Results

Results has been changed from previous version, so you will need to adapt how you process them. This change
follows the official Amazon Product Advertising API documentation, so you can
[check it](https://webservices.amazon.com/paapi5/documentation/operations.html) for reference. Just note that
documentation uses `CamelCase` names, but this module uses `snake_case`:

    ItemInfo.ContentInfo    ->  item_info.content_info
    Offers.Listings.Price   ->  offers.listings.price

Type hints has been added to the new version, so it is highly recommended to use an IDE that includes code
completion features, like [Visual Studio Code](https://code.visualstudio.com/).

### Throttling

Throttling parameter now represents the seconds to wait between API calls instead of the frequency. So make sure
to adapt the value to your needs.

```python
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=4)  # Makes 1 request every 4 seconds
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=0)  # No wait time between requests
```

### Serializer for Django

The serializer for Django is not available for this new version. If you want to help with the migration, send a
merge request and will be added on future updates.

### I need more help

You can always ask for help in our [Telegram group](https://t.me/PythonAmazonPAAPI) or raise an issue on
[Github](https://github.com/sergioteula/python-amazon-paapi/issues) for help. If you find that this
guide could be improved somehow, feel free to send a merge request with your changes.
