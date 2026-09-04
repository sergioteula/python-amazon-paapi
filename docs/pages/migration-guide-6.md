# Creators API migration guide

This guide explains how to migrate from the `amazon_paapi` module to the
`amazon_creatorsapi` module, which uses Amazon's Creators API.

## Why migrate?

Version 6.0.0 introduced support for Amazon's new **Creators API**, which replaces the
Product Advertising API (PAAPI). The old `amazon_paapi` module was deprecated in that
release and removed in 7.0.0, so importing it now raises `ModuleNotFoundError`.

Key benefits of the Creators API:

- OAuth2-based authentication (more secure)
- Simplified credential management
- New features and improvements from Amazon

## How to upgrade?

Upgrading to the last version of this module is as easy as running this pip command:

```bash
pip install python-amazon-paapi --upgrade
```

## Credential changes

The Creators API uses different credentials than PAAPI:

| PAAPI       | Creators API      |
| ----------- | ----------------- |
| Access Key  | Credential ID     |
| Secret Key  | Credential Secret |
| -           | Version           |
| Partner Tag | Partner Tag       |
| Country     | Country           |

You will need to obtain new credentials from the Amazon Associates Creators API portal.
The credentials are issued for a specific API version, which is a new value that PAAPI
did not have and that every client has to provide. See
[API versions](usage-guide.md#api-versions) for the accepted values.

## What should I change in my current code?

### Import changes

```diff
- from amazon_paapi import AmazonApi
+ from amazon_creatorsapi import AmazonCreatorsApi
```

### Initialization changes

```diff
- amazon = AmazonApi(
-     access_key="YOUR_ACCESS_KEY",
-     secret_key="YOUR_SECRET_KEY",
-     partner_tag="YOUR_TAG",
-     country="ES"
- )

+ amazon = AmazonCreatorsApi(
+     credential_id="YOUR_CREDENTIAL_ID",
+     credential_secret="YOUR_CREDENTIAL_SECRET",
+     version="2.2",
+     tag="YOUR_TAG",
+     country="ES"
+ )
```

### Method signature changes

The main methods keep their names, but some parameters are gone and a `resources`
parameter was added to every one of them, to choose which fields Amazon returns:

| Method             | Removed parameters      | Added parameters                          |
| ------------------ | ----------------------- | ----------------------------------------- |
| `get_items`        | `merchant`, `**kwargs`  | `resources: list[GetItemsResource]`        |
| `search_items`     | `merchant`, `**kwargs`  | `resources: list[SearchItemsResource]`     |
| `get_variations`   | `merchant`, `**kwargs`  | `resources: list[GetVariationsResource]`   |
| `get_browse_nodes` | `**kwargs`              | `resources: list[GetBrowseNodesResource]`  |

The `merchant` filter has no equivalent in the Creators API. The `**kwargs` catch-all is
gone on purpose: an unknown argument is now rejected by the signature instead of being
forwarded to Amazon and silently ignored.

Parameters such as `include_unavailable` in `get_items`, or `availability` and
`delivery_flags` in `search_items`, do exist in the Creators API and behave as they did
in PAAPI. See the [usage guide](usage-guide.md) for the complete signatures.

#### Basic usage examples

```python
# Get items
items = amazon.get_items(["B01N5IB20Q"])

# Search items
results = amazon.search_items(keywords="nintendo")

# Get variations
variations = amazon.get_variations("B01N5IB20Q")

# Get browse nodes
nodes = amazon.get_browse_nodes(["667049031"])
```

### Helper functions

```diff
- from amazon_paapi import get_asin
+ from amazon_creatorsapi import get_asin
```

### Models module

Version 6.0 introduced a `models` module that re-exports all SDK models for convenient
access:

```python
from amazon_creatorsapi.models import (
    Item,
    Condition,
    SortBy,
    GetItemsResource,
    SearchItemsResource,
    GetVariationsResource,
    GetBrowseNodesResource,
)
```

This allows you to import models directly without navigating the SDK structure.

### Exceptions

Exception names have changed to use the `Error` suffix, and every one of them inherits
from `AmazonCreatorsApiError`, so a single `except` covers them all:

```python
from amazon_creatorsapi.errors import (
    AmazonCreatorsApiError,  # Base exception
    AccessDeniedError,
    AssociateValidationError,
    AuthenticationError,
    InvalidArgumentError,
    ItemsNotFoundError,
    RequestError,
    ResourceNotFoundError,
    TooManyRequestsError,
)
```

See [Error handling](usage-guide.md#error-handling) for what raises each of them.

## I need more help

You can always ask for help in our [Telegram group](https://t.me/PythonAmazonPAAPI) or raise an issue on
[Github](https://github.com/sergioteula/python-amazon-paapi/issues) for help. If you find that this
guide could be improved somehow, feel free to send a pull request with your changes.
