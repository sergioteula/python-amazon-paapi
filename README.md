# Python Amazon Creators API

A Python wrapper for the [Amazon Creators API](https://webservices.amazon.com/creatorsapi/documentation/).

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-≥3.9-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Downloads)](https://pypi.org/project/python-amazon-paapi/)

## Features

- 🎯 **Simple object-oriented interface** for easy integration
- � **Async/await support** for high-performance applications
- �🔍 **Product search** by keywords, categories, or browse nodes
- 📦 **Product details** via ASIN or Amazon URL
- 🔄 **Item variations** support (size, color, etc.)
- 📊 **Feeds and reports** listing and download URLs
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

### Feeds and Reports

Feeds and reports are listed per marketplace, and downloaded through the
temporary URL returned by the API:

```python
from amazon_creatorsapi.models import FeedType, ReportType

for feed in api.list_feeds():
    print(feed.feed_name, feed.feed_type, feed.size)

url = api.get_feed("product-feed", feed_type=FeedType.PRODUCT_FEEDS)

for report in api.list_reports():
    print(report.filename, report.report_type, report.last_modified)

url = api.get_report("earnings.csv", report_type=ReportType.CREATOR_CONNECTIONS)
```

The type is only needed to disambiguate a name available in more than one
program, such as a report present in both Creator Central and Creator
Connections.

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

### Timeout

Timeout value represents the number of seconds to wait for a response before failing, being the default value 30 seconds. Use `None` to wait indefinitely.

```python
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, timeout=10)  # Fails after 10 seconds
amazon = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, timeout=0.5)  # Fails after half a second
```

It applies to every API request. In `AmazonCreatorsApi` the OAuth2 token refresh is handled by the bundled SDK and is not covered by this value, while `AsyncAmazonCreatorsApi` applies it to the token refresh as well.

### Async Support

For async/await applications, use the async version of the API with `httpx`:

```bash
pip install python-amazon-paapi[async] --upgrade
```

The async API provides the same methods as the synchronous version, but they must be called with `await`:

```python
from amazon_creatorsapi.aio import AsyncAmazonCreatorsApi
from amazon_creatorsapi import Country

# Use as async context manager (recommended for connection pooling)
async with AsyncAmazonCreatorsApi(
    credential_id="your_credential_id",
    credential_secret="your_credential_secret",
    version="2.2",
    tag="your-affiliate-tag",
    country=Country.US,
) as api:
    items = await api.get_items(["B01N5IB20Q"])
    results = await api.search_items(keywords="laptop")
    variations = await api.get_variations("B01N5IB20Q")
    nodes = await api.get_browse_nodes(["667049031"])
    feeds = await api.list_feeds()
    reports = await api.list_reports()

# Or use without context manager (creates new connection per request)
api = AsyncAmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY)
items = await api.get_items(["B01N5IB20Q"])
```

> **Note:** All synchronous methods and parameters work identically in async mode. Use `async with` for better performance when making multiple API calls.

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
