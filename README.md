# Python Amazon Creators API

A Python wrapper for Amazon's product APIs. This package supports both the legacy [Product Advertising API 5.0](https://webservices.amazon.com/paapi5/documentation/) and the new [Amazon Creators API](https://webservices.amazon.com/creatorsapi/documentation/).

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-≥3.9-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Downloads)](https://pypi.org/project/python-amazon-paapi/)

> [!IMPORTANT]
> **Migration Advisory**: The `amazon_paapi` module is deprecated. Amazon is transitioning from the Product Advertising API (PAAPI) to the new **Creators API**. Please migrate to the `amazon_creatorsapi` module for new projects. See the [Migration Guide](https://python-amazon-paapi.readthedocs.io/en/latest/pages/migration-guide-6.html) for more information.

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

## Quick Start

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

## Usage Examples

### Get Multiple Items

```python
items = api.get_items(["B01N5IB20Q", "B01F9G43WU"])
for item in items:
    print(item.images.primary.large.url)
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

### Get the ASIN from URL

```python
from amazon_creatorsapi import get_asin

asin = get_asin("https://www.amazon.com/dp/B01N5IB20Q")
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

### Throttling

Throttling value represents the wait time in seconds between API calls, being the default value 1 second. Use it to avoid reaching Amazon request limits.

```python
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=4)  # Makes 1 request every 4 seconds
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=0)  # No wait time between requests
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
