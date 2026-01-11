# Installation

You can install or upgrade the module with:

    pip install python-amazon-paapi --upgrade

# Usage guide

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

**Use URL instead of ASIN:**

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
