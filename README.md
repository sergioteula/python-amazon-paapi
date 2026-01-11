# Python Amazon PAAPI

A simple Python wrapper for the [Amazon Product Advertising API 5.0](https://webservices.amazon.com/paapi5/documentation/). Easily interact with Amazon's official API to retrieve product information, search for items, and more.

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-≥3.9-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Amazon API](https://img.shields.io/badge/Amazon%20API-5.0-%23FD9B15)](https://webservices.amazon.com/paapi5/documentation/)
[![Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Downloads)](https://pypi.org/project/python-amazon-paapi/)

## Features

- 🎯 **Simple object-oriented interface** for easy integration
- 🔍 **Product search** by keywords, categories, or browse nodes
- 📦 **Product details** via ASIN or Amazon URL
- 🔄 **Item variations** support (size, color, etc.)
- 💰 **OffersV2 support** for enhanced pricing and offer details
- 🌍 **20+ countries** supported ([full list](https://github.com/sergioteula/python-amazon-paapi/blob/master/amazon_paapi/models/regions.py))
- ⚡ **Batch requests** to get multiple items without the 10-item limit
- 🛡️ **Built-in throttling** to avoid API rate limits
- 📝 **Full type hints** for better IDE support

## Installation

```bash
pip install python-amazon-paapi --upgrade
```

## Quick Start

```python
from amazon_paapi import AmazonApi

# Initialize the API (get credentials from Amazon Associates)
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY)

# Get product information by ASIN
item = amazon.get_items('B01N5IB20Q')[0]
print(item.item_info.title.display_value)
```

## Usage Examples

### Using OffersV2 resources

OffersV2 provides enhanced pricing and offer details. All resources are included by default, so OffersV2 data is available without any additional configuration:

```python
item = amazon.get_items('B01N5IB20Q')[0]
if item.offers_v2 and item.offers_v2.listings:
    listing = item.offers_v2.listings[0]
    print(listing.price.money.amount)  # Price amount
    print(listing.merchant_info.name)  # Merchant name
```

### Get Multiple Products

```python
items = amazon.get_items(['B01N5IB20Q', 'B01F9G43WU'])
for item in items:
    print(item.images.primary.large.url)
    print(item.offers.listings[0].price.amount)
```

### Use Amazon URL Instead of ASIN

```python
item = amazon.get_items('https://www.amazon.com/dp/B01N5IB20Q')
```

### Search Products

```python
results = amazon.search_items(keywords='nintendo switch')
for item in results.items:
    print(item.item_info.title.display_value)
```

### Get Product Variations

```python
variations = amazon.get_variations('B01N5IB20Q')
for item in variations.items:
    print(item.detail_page_url)
```

### Get Browse Node Information

```python
nodes = amazon.get_browse_nodes(['667049031', '599385031'])
for node in nodes:
    print(node.display_name)
```

### Extract ASIN from URL

```python
from amazon_paapi import get_asin

asin = get_asin('https://www.amazon.com/dp/B01N5IB20Q')
# Returns: 'B01N5IB20Q'
```

### Configure Throttling

Control the wait time between API calls to avoid rate limits:

```python
# Wait 4 seconds between requests
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=4)

# No throttling (use with caution)
amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY, throttling=0)
```

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

3. Copy `.env.template` to `.env` and add your Amazon API credentials for integration tests.

Pre-commit hooks will automatically run Ruff, mypy, and tests before each commit.

## License

MIT License © 2026 [Sergio Abad](https://github.com/sergioteula)
