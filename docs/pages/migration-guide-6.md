# Creators API migration guide

This guide explains how to migrate from the deprecated `amazon_paapi` module to the new
`amazon_creatorsapi` module, which uses Amazon's Creators API.

## Why migrate?

Version 6.0.0 introduces support for Amazon's new **Creators API**, which replaces the
Product Advertising API (PAAPI). The old `amazon_paapi` module is now deprecated and will
not receive new features.

Key benefits of the Creators API:

- OAuth2-based authentication (more secure)
- Simplified credential management
- New features and improvements from Amazon

## Changelog summary

- New `amazon_creatorsapi` module for the Creators API
- The `amazon_paapi` module is deprecated (shows a warning when imported)
- Different authentication credentials required

## How to upgrade?

Upgrading to the last version of this module is as easy as running this pip command:

    pip install python-amazon-paapi --upgrade

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

While the main methods have the same names, there are important parameter differences:

#### `get_items`

| Removed in Creators API | New in Creators API                 |
| ----------------------- | ----------------------------------- |
| `merchant`              | `resources: list[GetItemsResource]` |
| `include_unavailable`   |                                     |
| `**kwargs`              |                                     |

#### `search_items`

| Removed in Creators API | New in Creators API                    |
| ----------------------- | -------------------------------------- |
| `availability`          | `resources: list[SearchItemsResource]` |
| `delivery_flags`        |                                        |
| `merchant`              |                                        |
| `**kwargs`              |                                        |

#### `get_variations`

| Removed in Creators API | New in Creators API                      |
| ----------------------- | ---------------------------------------- |
| `merchant`              | `resources: list[GetVariationsResource]` |
| `**kwargs`              |                                          |

#### `get_browse_nodes`

| Removed in Creators API | New in Creators API                       |
| ----------------------- | ----------------------------------------- |
| `**kwargs`              | `resources: list[GetBrowseNodesResource]` |

#### Basic usage examples

```python
# Get items
items = amazon.get_items(['B01N5IB20Q'])

# Search items
results = amazon.search_items(keywords='nintendo')

# Get variations
variations = amazon.get_variations('B01N5IB20Q')

# Get browse nodes
nodes = amazon.get_browse_nodes(['667049031'])
```

### Helper functions

```diff
- from amazon_paapi import get_asin
+ from amazon_creatorsapi.core import get_asin
```

### Models module

Version 6.0 introduces a new `models` module that re-exports all SDK models for convenient access:

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

Exception names have changed to use the `Error` suffix:

```python
from amazon_creatorsapi.errors import (
    AmazonCreatorsApiError,      # Base exception
    InvalidArgumentError,
    ItemsNotFoundError,
    TooManyRequestsError,
    AssociateValidationError,
    RequestError,
)
```

## I need more help

You can always ask for help in our [Telegram group](https://t.me/PythonAmazonPAAPI) or raise an issue on
[Github](https://github.com/sergioteula/python-amazon-paapi/issues) for help. If you find that this
guide could be improved somehow, feel free to send a pull request with your changes.
