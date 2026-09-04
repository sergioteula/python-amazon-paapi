# Python Amazon Creators API

A Python wrapper for the [Amazon Creators API](https://webservices.amazon.com/creatorsapi/documentation/).

[![PyPI](https://img.shields.io/pypi/v/python-amazon-paapi?color=%231182C2&label=PyPI)](https://pypi.org/project/python-amazon-paapi/)
[![Python](https://img.shields.io/badge/Python-≥3.9-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-amazon-paapi/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/python-amazon-paapi?label=Downloads)](https://pypi.org/project/python-amazon-paapi/)

## Features

- 🎯 **Simple object-oriented interface** for easy integration
- ⚡ **Async/await support** for high-performance applications
- 🔍 **Product search** by keywords, categories, or browse nodes
- 📦 **Product details** via ASIN or Amazon URL
- 🔄 **Item variations** support (size, color, etc.)
- 📊 **Feeds and reports** listing and download URLs
- 💰 **OffersV2 support** for enhanced pricing and offer details
- 🌍 **20 marketplaces** supported
- 🛡️ **Built-in throttling and retries** to avoid API rate limits
- 📝 **Full type hints** for better IDE support

## Table of contents

- [Installation](#installation)
- [Credentials](#credentials)
- [Quick start](#quick-start)
- [Usage examples](#usage-examples)
- [Configuration](#configuration)
- [Error handling](#error-handling)
- [Async support](#async-support)
- [Working with models](#working-with-models)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Installation

```bash
pip install python-amazon-paapi --upgrade
```

Python 3.9 or newer is required. Install the `async` extra to use the asynchronous
client:

```bash
pip install python-amazon-paapi[async] --upgrade
```

## Credentials

Four values are needed to create a client, and all of them come from the Amazon
Associates Creators API portal:

| Argument            | What it is                                                |
| ------------------- | --------------------------------------------------------- |
| `credential_id`     | Identifier of your Creators API credentials               |
| `credential_secret` | Secret of your Creators API credentials                   |
| `version`           | API version your credentials were issued for              |
| `tag`               | Your affiliate tracking id, also known as the partner tag |

`version` is the version of the Creators API, not of this library: it is the value Amazon
gave you along with the credentials, and it also decides which endpoint issues the OAuth2
token. The accepted values are `2.1`, `2.2`, `2.3`, `3.1`, `3.2` and `3.3`; any other one
raises `ValueError` when the client is created.

The marketplace is chosen with `country`, which accepts `AU`, `BE`, `BR`, `CA`, `DE`,
`ES`, `FR`, `IN`, `IT`, `JP`, `MX`, `NL`, `PL`, `SA`, `SE`, `SG`, `TR`, `UK`, `US` and
`AE`, either as a string or through the `Country` constants. Pass `marketplace` instead
to give the host directly, such as `marketplace="www.amazon.es"`.

## Quick start

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

Every field of a response is optional, as Amazon only sends what it has for an item, so
check a value before using it when the item may not carry it.

## Usage examples

### Get multiple items

```python
items = api.get_items(["B01N5IB20Q", "B01F9G43WU"])
for item in items:
    print(item.images.primary.large.url)
```

Items come back in the order they were requested, duplicates are asked for
only once, and requests with more items than the API accepts at once (10) are
split into as many calls as needed, so any amount of items can be requested:

```python
items = api.get_items(asins)  # Any amount of items, split into several calls
```

Amazon can answer with only some of the requested items, describing the
missing ones as partial errors. Those errors are available in the returned
list, and unavailable items can be included as an item holding only the ASIN:

```python
items = api.get_items(["B01N5IB20Q", "0000000000"], include_unavailable=True)

for error in items.errors:
    print(error.code, error.message)

for item in items:
    if item.item_info is None:
        print(f"{item.asin} is not available")
```

### Search products

```python
results = api.search_items(keywords="nintendo switch")
for item in results.items:
    print(item.item_info.title.display_value)
```

A search needs at least one of `keywords`, `actor`, `artist`, `author`, `brand`, `title`,
`browse_node_id` or `search_index`, and only returns the items available for purchase
unless asked otherwise:

```python
from amazon_creatorsapi.models import Availability

results = api.search_items(
    keywords="nintendo switch",
    availability=Availability.INCLUDEOUTOFSTOCK,
)
```

### Get product variations

```python
# Using ASIN
variations = api.get_variations("B01N5IB20Q")

# Or using Amazon URL
variations = api.get_variations("https://www.amazon.com/dp/B01N5IB20Q")

for item in variations.items:
    print(item.detail_page_url)
```

### Get browse node information

```python
nodes = api.get_browse_nodes(["667049031"])
for node in nodes:
    print(node.display_name)
```

### Feeds and reports

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

### Using OffersV2 resources

```python
items = api.get_items(["B01N5IB20Q"])
item = items[0]
if item.offers_v2 and item.offers_v2.listings:
    listing = item.offers_v2.listings[0]
    print(listing.price.money.amount)
    print(listing.merchant_info.name)
```

## Configuration

### Throttling

Throttling value represents the wait time in seconds between API calls, being the default
value 1 second. Use it to avoid reaching Amazon request limits.

```python
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=4)  # Makes 1 request every 4 seconds
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, throttling=0)  # No wait time between requests
```

The interval is kept per client and is safe to share between threads.

### Timeout

Timeout value represents the number of seconds to wait for a response before failing,
being the default value 30 seconds. Use `None` to wait indefinitely.

```python
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, timeout=10)  # Fails after 10 seconds
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, timeout=0.5)  # Fails after half a second
```

It applies to every API request, including the OAuth2 token refresh.

### Retries

Amazon asks clients to back off and try again when it throttles a request or fails to
serve it. The client does that on its own, waiting longer before every attempt and
honouring the `Retry-After` header when the API sends it. An expired token is refreshed
once and the request is sent again.

```python
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, retries=5)  # Up to 5 extra attempts
api = AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY, retries=0)  # Fail on the first error
```

The default is 3 extra attempts, and only the failures that Amazon asks to retry are
retried: a rejected request fails right away.

### Closing the client

The client keeps a pool of connections open, so it is meant to be created once and
reused. Close it, or use it as a context manager, when it is not going to be used again:

```python
with AmazonCreatorsApi(ID, SECRET, VERSION, TAG, COUNTRY) as api:
    items = api.get_items(["B01N5IB20Q"])
```

### Custom endpoints

The base URL of the API and the one used to get the OAuth2 token can be replaced, which
is useful to run the tests of a project against a mock server. Providing `auth_endpoint`
also makes valid a `version` that is not in the list yet, so a new one can be used before
the library knows about it, as long as it belongs to a family that the library can
authenticate: `2.x` with Cognito and `3.x` with Login with Amazon. A version of any other
family is rejected, as a new family brings a new authentication flow and not just another
endpoint:

```python
api = AmazonCreatorsApi(
    ID,
    SECRET,
    VERSION,
    TAG,
    COUNTRY,
    host="http://localhost:8080",
    auth_endpoint="http://localhost:8080/token",
)
```

## Error handling

Every error raised by the library inherits from `AmazonCreatorsApiError`, so a single
`except` covers them all. The message carries the reason given by Amazon, the fields that
failed validation and the identifier of the request, which is what Amazon support asks
for:

| Exception | Raised when |
| --- | --- |
| `InvalidArgumentError` | An argument is not valid or the request is rejected by Amazon |
| `AssociateValidationError` | The credentials are not valid for the selected marketplace |
| `AuthenticationError` | The credentials are missing, invalid or expired |
| `AccessDeniedError` | The credentials cannot perform the requested operation |
| `ItemsNotFoundError` | No items are found for the request |
| `ResourceNotFoundError` | The requested feed or report does not exist |
| `TooManyRequestsError` | The rate limit is exceeded and the retries are exhausted |
| `RequestError` | The request fails for any other reason |

```python
from amazon_creatorsapi.errors import AmazonCreatorsApiError, ItemsNotFoundError

try:
    items = api.get_items(["B01N5IB20Q"])
except ItemsNotFoundError:
    print("The item is not available")
except AmazonCreatorsApiError as error:
    print(error)
```

## Async support

For async/await applications, use the async version of the API with `httpx`:

```bash
pip install python-amazon-paapi[async] --upgrade
```

The async API provides the same methods, parameters and errors as the synchronous
version, and they are called with `await`:

```python
from amazon_creatorsapi import Country
from amazon_creatorsapi.aio import AsyncAmazonCreatorsApi

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

> **Note:** outside `async with`, every request opens and closes its own connection, so
> there is nothing to release and the async client has no `close` method. Use
> `async with` when making more than one call, to keep the connection open between them.

## Working with models

All SDK models are re-exported through `amazon_creatorsapi.models` for convenient access:

```python
from amazon_creatorsapi.models import (
    Condition,
    GetItemsResource,
    Item,
    SearchItemsResource,
    SortBy,
)

# Use Condition enum for filtering
items = api.get_items(["B01N5IB20Q"], condition=Condition.NEW)

# Use SortBy enum for search ordering
results = api.search_items(
    keywords="laptop",
    sort_by=SortBy.PRICE_COLON_LOW_TO_HIGH,
)

# Specify which resources to retrieve
resources = [
    GetItemsResource.ITEM_INFO_DOT_TITLE,
    GetItemsResource.OFFERS_V2_DOT_LISTINGS_DOT_PRICE,
]
items = api.get_items(["B01N5IB20Q"], resources=resources)
```

Every method asks for all the resources of its operation when `resources` is not given.
Narrowing the list makes the response smaller and faster, and the fields left out come
back as `None`.

---

## Documentation

- 📖 [Full documentation](https://python-amazon-paapi.readthedocs.io/)
- 📘 [Usage guide](https://python-amazon-paapi.readthedocs.io/en/latest/pages/usage-guide.html)
- 🔀 [Migration guide from `amazon_paapi`](https://python-amazon-paapi.readthedocs.io/en/latest/pages/migration-guide-6.html)
- 📋 [Changelog](https://github.com/sergioteula/python-amazon-paapi/blob/master/CHANGELOG.md)
- 💬 [Telegram support group](https://t.me/PythonAmazonPAAPI)

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, or
get started with:

```bash
git clone https://github.com/sergioteula/python-amazon-paapi.git
cd python-amazon-paapi
uv sync --extra async
make setup
make test
```

Pre-commit hooks run Ruff, mypy and the tests before each commit.

## License

MIT License © 2026 [Sergio Abad](https://github.com/sergioteula)
