# Version 7 migration guide

This guide covers what can break in code written for `amazon_creatorsapi` on version 6
when upgrading to version 7. If you are still importing the removed `amazon_paapi`
module, read the [Creators API migration guide](migration-guide-6.md) first: that is a
rewrite, and this guide starts where it ends.

Most code needs no change at all. Skip to [Nothing to do](#nothing-to-do) to rule out
the changes that look breaking and are not.

## At a glance

| Change | Breaks | Fix |
| --- | --- | --- |
| A rejected request raises `InvalidArgumentError` | `except RequestError` around a `400` | Catch `AmazonCreatorsApiError`, or add `InvalidArgumentError` |
| Values are validated before the request | `except pydantic.ValidationError` | Catch `InvalidArgumentError` |
| The async client validates like the synchronous one | Values out of the ranges of the API | Send values the API accepts |
| `search_items` needs a criterion | A search with only filters | Add `keywords` or any other criterion |
| `get_items` raises when nothing is found | `if not items:` | Catch `ItemsNotFoundError`, or use `include_unavailable` |
| `get_items` returns the requested order | Reading the response by position | Read it by position, or match by `asin` |
| The synchronous client times out | Requests above 30 seconds | Pass `timeout` |
| Failed requests are retried | Handling a `429` yourself | Pass `retries=0` |
| `get_asin` rejects a long identifier | Malformed URLs | Fix the URLs |
| The version is validated on creation | An unsupported `version` | Use a supported one, or pass `auth_endpoint` |
| Every client has its own SDK configuration | `Configuration.set_default()` | Pass `host` |

## Errors

The errors are now taken from the response of the Creators API instead of the codes of
the old Product Advertising API, so each failure has the type that describes it:

| Status | Version 6 | Version 7 |
| --- | --- | --- |
| `400` | `InvalidArgumentError` or `RequestError` | `InvalidArgumentError` |
| `400` for an invalid associate | `AssociateValidationError` | `AssociateValidationError` |
| `401` | `RequestError` | `AuthenticationError` |
| `403` | `RequestError` | `AccessDeniedError` |
| `404` | `ItemsNotFoundError` | `ItemsNotFoundError`, or `ResourceNotFoundError` for feeds and reports |
| `429` | `TooManyRequestsError` | `TooManyRequestsError` |
| Anything else | `RequestError` | `RequestError` |

`AuthenticationError` and `AccessDeniedError` are subclasses of `RequestError`, so code
catching `RequestError` keeps working for `401` and `403`. The one case that changes is
a `400` whose body did not name the invalid parameter, which used to be a `RequestError`
and is now an `InvalidArgumentError`:

```python
from amazon_creatorsapi.errors import AmazonCreatorsApiError

try:
    items = api.get_items(["B01N5IB20Q"])
except AmazonCreatorsApiError as error:  # Catches every error of the library
    print(error)
```

The message of an error now carries the reason given by Amazon, the fields it rejected
and the identifier of the request, so any code matching on the text of a message has to
be reviewed.

## Invalid values

Values rejected by the constraints of the API raise `InvalidArgumentError` instead of
the `ValidationError` of pydantic, so the library no longer leaks the errors of its
dependencies:

```python
from amazon_creatorsapi.errors import InvalidArgumentError

try:
    api.search_items(keywords="laptop", min_reviews_rating=5)
except InvalidArgumentError as error:
    print(error)  # Invalid parameters for the request: minReviewsRating: ...
```

`InvalidArgumentError` is also a `ValueError`, which `pydantic.ValidationError` is too,
so an `except ValueError` written for version 6 keeps catching it. Only the code
catching `pydantic.ValidationError` by name has to be changed.

The asynchronous client used to send its requests without validating them, so it
accepted values that Amazon rejected. It now validates the same values as the
synchronous one, and a request that used to fail with a `400` fails locally instead:

| Argument | Accepted |
| --- | --- |
| `item_count` | 1 to 100 |
| `item_page` | 1 to 10 |
| `variation_count` | 1 to 10 |
| `variation_page` | 1 or greater |
| `min_reviews_rating` | 1 to 4 |
| `min_saving_percent` | 1 to 99 |
| `max_price`, `min_price` | 1 or greater |

`throttling`, `timeout` and `retries` are validated as well, so a negative or
non-numeric value raises `InvalidArgumentError` when the client is created instead of
failing later with a `TypeError`.

## Searching without a criterion

`search_items` needs at least one of `keywords`, `actor`, `artist`, `author`, `brand`,
`title`, `browse_node_id` or `search_index`. A search carrying only filters used to be
sent to Amazon and now raises `InvalidArgumentError`:

```python
api.search_items(min_price=1000)                     # InvalidArgumentError
api.search_items(keywords="laptop", min_price=1000)  # Correct
```

## Items that are not found

`get_items` raises `ItemsNotFoundError` when the response holds none of the requested
items, as it was documented to do and as `search_items` already did. It used to return
an empty list in some responses:

```python
from amazon_creatorsapi.errors import ItemsNotFoundError

try:
    items = api.get_items(["B01N5IB20Q", "0000000000"])
except ItemsNotFoundError as error:
    items = []
```

To get a result without handling the exception, ask for the missing items as well. Every
identifier that Amazon did not return comes back as an `Item` holding only its `asin`:

```python
items = api.get_items(["B01N5IB20Q", "0000000000"], include_unavailable=True)
```

Either way, the reason for every missing item is available in the `errors` attribute of
the returned list:

```python
for error in items.errors:
    print(error.code, error.message)
```

## The order of the items

`get_items` returns the items in the order they were requested, instead of the order
Amazon sent them in, and asks for duplicated identifiers only once. Reading the response
by position is now correct, but the length of the list still does not have to match the
amount of identifiers, as Amazon can leave items out:

```python
items = api.get_items(["B01N5IB20Q", "B01N5IB20Q", "0000000000"])
len(items)  # 1, not 3

items = api.get_items(["B01N5IB20Q", "0000000000"], include_unavailable=True)
len(items)  # 2, one item per identifier, in the order they were requested
```

`get_items` also splits a request with more than ten identifiers into as many calls as
needed, so it no longer fails for a long list. Keep in mind that a call is sent for
every ten items, each one waiting for the configured `throttling`.

## Timeouts

The synchronous client waited indefinitely for a response. It now uses the same 30
second timeout that the asynchronous one already had:

```python
api = AmazonCreatorsApi(..., timeout=60)    # Wait up to a minute
api = AmazonCreatorsApi(..., timeout=None)  # Wait indefinitely, as version 6 did
```

The timeout applies to each request, so a `get_items` split into several calls gets the
whole timeout for each one of them.

## Retries

Both clients retry the requests that Amazon asks to retry, which are the ones failing
with `429`, `500`, `502`, `503` and `504`. Every attempt waits longer than the previous
one, honouring the `Retry-After` header when the response carries it, up to 30 seconds
per wait.

The type of the error does not change, so nothing has to be caught differently, but a
throttled call now takes longer before raising `TooManyRequestsError`. Disable the
retries to get the behaviour of version 6, which is what you want if your code already
implements its own backoff:

```python
api = AmazonCreatorsApi(..., retries=0)
```

## ASINs in URLs

`get_asin`, used by `get_items` for every identifier it receives, no longer trims an
identifier longer than ten characters. A URL such as `.../dp/B01N5IB20Q12` used to
return `B01N5IB20Q`, which is a different item, and now raises `InvalidArgumentError`.
Malformed URLs that silently returned the wrong item have to be fixed.

## Versions

Both clients resolve the auth endpoint from the same list of versions, and the
synchronous one validates the version when it is created instead of failing on the first
request. The error is an `InvalidArgumentError`, which is a `ValueError`, so an
`except ValueError` written for version 6 keeps working.

A version of a family the library knows how to authenticate, which are `2.x` and `3.x`,
can be used before the library lists it by providing its endpoint:

```python
api = AmazonCreatorsApi(
    ...,
    version="2.4",
    auth_endpoint="https://creatorsapi.auth.eu-west-1.amazoncognito.com/oauth2/token",
)
```

## The configuration of the SDK

Every client now builds its own configuration for the bundled SDK, instead of sharing
the one the SDK keeps for the whole process. Two clients in the same program no longer
overwrite each other, and a `Configuration.set_default()` no longer reaches them. Use
the `host` argument to send the requests somewhere else, which is useful to run tests
against a mock server:

```python
api = AmazonCreatorsApi(..., host="http://localhost:8080")
```

The `auth_endpoint` argument does the same for the requests asking for a token.

## Nothing to do

These changes look breaking and are not:

- `get_items` and `get_browse_nodes` return a `ResultList`, which is a `list` carrying
  the partial errors of the response in its `errors` attribute. It behaves like any
  other list.
- The arguments of `search_items` keep the position they had in version 6. `availability`
  was added as a keyword only argument, after the rest, so it cannot displace them.
- `except RequestError` still catches the failures of a request that got a `401` or a
  `403`, and `except ValueError` still catches an invalid value.
- Requesting more than ten items at once works instead of failing.
- The exceptions of the library are all subclasses of `AmazonCreatorsApiError`, which is
  the safest thing to catch.

## New in version 7

Nothing here breaks existing code, but it may replace it:

- `AmazonCreatorsApi` closes its connections with `close()` or as a context manager,
  which the asynchronous client already supported.
- `list_feeds`, `get_feed`, `list_reports` and `get_report` in both clients.
- `availability` in `search_items`, to include the items that are out of stock.
- `errors` and `get_asin` are available directly in `amazon_creatorsapi`.
- The package ships a `py.typed` marker, so type checkers use its type hints.
