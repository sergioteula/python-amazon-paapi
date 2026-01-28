# Installation

You can install or upgrade the module with:

    pip install python-amazon-paapi --upgrade

# Usage Guide

The new `amazon_creatorsapi` module provides access to Amazon's Creators API.

> **Note:** The `amazon_paapi` module is deprecated. New projects should use the Creators API.

**Basic usage:**

```python
from amazon_creatorsapi import AmazonCreatorsApi, Country

amazon = AmazonCreatorsApi(
    credential_id='YOUR_CREDENTIAL_ID',
    credential_secret='YOUR_CREDENTIAL_SECRET',
    version='2.2',
    tag='YOUR_TAG',
    country=Country.US
)

item = amazon.get_items('B01N5IB20Q')[0]
print(item.item_info.title.display_value)  # Item title
```

**Get multiple items information:**

```python
items = amazon.get_items(['B01N5IB20Q', 'B01F9G43WU'])
for item in items:
    print(item.images.primary.large.url)  # Primary image url
```

**Search items:**

```python
search_result = amazon.search_items(keywords='nintendo')
for item in search_result.items:
    print(item.asin)  # Item ASIN
```

**Get item variations:**

```python
variations = amazon.get_variations('B01N5IB20Q')
for item in variations.items:
    print(item.detail_page_url)  # Affiliate url
```

**Get the ASIN from URL:**

```python
from amazon_creatorsapi.core import get_asin

asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')
```

**Throttling:**

Throttling value represents the wait time in seconds between API calls, being the default value 1 second. Use it to avoid reaching Amazon request limits.

```python
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=4)  # Makes 1 request every 4 seconds
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=0)  # No wait time between requests
```

**Working with Models:**

All SDK models are available through the `models` module for convenient access:

```python
from amazon_creatorsapi.models import (
    Item,
    Condition,
    SortBy,
    GetItemsResource,
    SearchItemsResource,
)

# Use Condition enum for filtering
items = amazon.get_items(['B01N5IB20Q'], condition=Condition.NEW)

# Use SortBy enum for search ordering
results = amazon.search_items(keywords='laptop', sort_by=SortBy.PRICE_LOW_TO_HIGH)

# Specify which resources to retrieve
resources = [GetItemsResource.ITEMINFO_TITLE, GetItemsResource.OFFERS_LISTINGS_PRICE]
items = amazon.get_items(['B01N5IB20Q'], resources=resources)
```

**Using OffersV2 resources:**

OffersV2 provides enhanced pricing and offer details. All resources are included by default, so OffersV2 data is available without any additional configuration:

```python
items = amazon.get_items('B01N5IB20Q')

# Access OffersV2 data
item = items[0]
if item.offers_v2 and item.offers_v2.listings:
    listing = item.offers_v2.listings[0]
    print(listing.price.money.amount)  # Price amount
    print(listing.merchant_info.name)  # Merchant name
```
