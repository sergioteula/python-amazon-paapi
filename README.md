# Python Amazon Creators API

A Python wrapper for Amazon's product APIs. This package supports both the legacy [Product Advertising API 5.0](https://webservices.amazon.com/paapi5/documentation/) and the new [Amazon Creators API](https://webservices.amazon.com/creatorsapi/documentation/).

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-≥3.9-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Downloads)](https://pypi.org/project/python-amazon-paapi/)

> [!IMPORTANT]
> **Migration Advisory**: The `amazon_paapi` module is deprecated. Amazon is transitioning from the Product Advertising API (PAAPI) to the new **Creators API**. Please migrate to the `amazon_creatorsapi` module for new projects. See the [Migration Guide](#migration-from-paapi-to-creators-api) below.

## Features

- 🎯 **Simple object-oriented interface** for easy integration
- 🔍 **Product search** by keywords, categories, or browse nodes
- 📦 **Product details** via ASIN or Amazon URL
- 🔄 **Item variations** support (size, color, etc.)
- 💰 **OffersV2 support** for enhanced pricing and offer details
- 🌍 **20+ countries** supported
- 🛡️ **Built-in throttling** to avoid API rate limits
- 📝 **Full type hints** for better IDE support

## Installation

```bash
pip install python-amazon-paapi --upgrade
```

---

## Amazon Creators API (Recommended)

The Creators API is Amazon's new API for affiliate product data, designed to replace the legacy PAAPI.

### Quick Start

```python
from amazon_creatorsapi import AmazonCreatorsApi, Country

# Initialize with your Creators API credentials
api = AmazonCreatorsApi(
    credential_id="your_credential_id",
    credential_secret="your_credential_secret",
    version="2.2",
    tag="your-affiliate-tag",
    country=Country.US,
)

# Get product information by ASIN
items = api.get_items(["B01N5IB20Q"])
print(items[0].item_info.title.display_value)

# Or use Amazon URLs directly
items = api.get_items(["https://www.amazon.com/dp/B01N5IB20Q"])
```

### Search Products

```python
results = api.search_items(keywords="nintendo switch")
for item in results.items:
    print(item.item_info.title.display_value)
```

### Get Product Variations

```python
# Using ASIN
variations = api.get_variations("B01N5IB20Q")

# Or using Amazon URL
variations = api.get_variations("https://www.amazon.com/dp/B01N5IB20Q")

for item in variations.items:
    print(item.detail_page_url)
```

### Get Browse Node Information

```python
nodes = api.get_browse_nodes(["667049031"])
for node in nodes:
    print(node.display_name)
```

### Using OffersV2 Resources

```python
items = api.get_items(["B01N5IB20Q"])
item = items[0]
if item.offers_v2 and item.offers_v2.listings:
    listing = item.offers_v2.listings[0]
    print(listing.price.money.amount)
    print(listing.merchant_info.name)
```

### Working with Models

All SDK models are re-exported through `amazon_creatorsapi.models` for convenient access:

```python
from amazon_creatorsapi.models import (
    Item,
    Condition,
    SortBy,
    GetItemsResource,
    SearchItemsResource,
)

# Use Condition enum for filtering
items = api.get_items(["B01N5IB20Q"], condition=Condition.NEW)

# Use SortBy enum for search ordering
results = api.search_items(keywords="laptop", sort_by=SortBy.PRICE_LOW_TO_HIGH)

# Specify which resources to retrieve
from amazon_creatorsapi.models import GetItemsResource
resources = [GetItemsResource.ITEMINFO_TITLE, GetItemsResource.OFFERS_LISTINGS_PRICE]
items = api.get_items(["B01N5IB20Q"], resources=resources)
```

## Legacy PAAPI (Deprecated)

> [!WARNING]
> The `amazon_paapi` module is deprecated and will be removed in a future version. Please migrate to `amazon_creatorsapi`.

### Quick Start

```python
from amazon_paapi import AmazonApi

amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY)
item = amazon.get_items('B01N5IB20Q')[0]
print(item.item_info.title.display_value)
```

### Usage Examples

<details>
<summary>Click to expand legacy PAAPI examples</summary>

#### Get Multiple Products

```python
items = amazon.get_items(['B01N5IB20Q', 'B01F9G43WU'])
for item in items:
    print(item.images.primary.large.url)
```

#### Use Amazon URL Instead of ASIN

```python
item = amazon.get_items('https://www.amazon.com/dp/B01N5IB20Q')
```

#### Search Products

```python
results = amazon.search_items(keywords='nintendo switch')
for item in results.items:
    print(item.item_info.title.display_value)
```

#### Extract ASIN from URL

```python
from amazon_paapi import get_asin

asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')
# Returns: 'B01N5IB20Q'
```

#### Configure Throttling

```python
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=4)
```

</details>

---

## Migration from PAAPI to Creators API

### Code Changes

**Before (PAAPI):**

```python
from amazon_paapi import AmazonApi

amazon = AmazonApi(api_key, api_secret, tag, country)
items = amazon.get_items('B01N5IB20Q')
```

**After (Creators API):**

```python
from amazon_creatorsapi import AmazonCreatorsApi

api = AmazonCreatorsApi(
    credential_id=credential_id,
    credential_secret=credential_secret,
    version="2.2",
    tag=tag,
    country=country,
)
items = api.get_items(["B01N5IB20Q"])
```

---

## Documentation

- 📖 [Full Documentation](https://python-amazon-paapi.readthedocs.io/)
- 📋 [Changelog](https://github.com/sergioteula/python-amazon-paapi/blob/master/CHANGELOG.md)
- 💬 [Telegram Support Group](https://t.me/PythonAmazonPAAPI)

## Contributing

Contributions are welcome! To get started:

1. Install [uv](https://docs.astral.sh/uv/) package manager
2. Clone and set up the project:

```bash
git clone https://github.com/sergioteula/python-amazon-paapi.git
cd python-amazon-paapi
uv sync
uv run pre-commit install
```

3. Copy `.env.template` to `.env` and add your API credentials for integration tests.

Pre-commit hooks will automatically run Ruff, mypy, and tests before each commit.

## License

MIT License © 2026 [Sergio Abad](https://github.com/sergioteula)
