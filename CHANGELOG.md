# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.0.0] - 2026-09-04

### Added

- `list_feeds`, `get_feed`, `list_reports` and `get_report` methods in `amazon_creatorsapi` and `amazon_creatorsapi.aio`, with `Feed`, `FeedType`, `ReportMetadata` and `ReportType` in `amazon_creatorsapi.models` and in the bundled SDK
- `timeout` parameter in `AmazonCreatorsApi` and `AsyncAmazonCreatorsApi` to set the request timeout in seconds, or `None` to wait indefinitely
- `retries` parameter in `AmazonCreatorsApi` and `AsyncAmazonCreatorsApi` to retry the throttled and failed requests that Amazon asks to retry, waiting longer before every attempt and honouring the `Retry-After` header, whether Amazon sends it as an amount of seconds or as a date
- `include_unavailable` parameter in `get_items` to get an item holding only the ASIN for every requested item missing from the response
- `availability` parameter in `search_items` to include the items that are out of stock, keyword only and placed after the rest, so the arguments of a caller not using keywords keep their position
- `host` and `auth_endpoint` parameters in `AmazonCreatorsApi` and `AsyncAmazonCreatorsApi` to replace the endpoints of the API, useful to run tests against a mock server or to use a version newer than the ones known by the library, as long as the library can authenticate its family
- `AccessDeniedError`, raised when the credentials cannot perform the requested operation
- `ResourceNotFoundError`, raised when a feed or report does not exist, telling it apart from missing items
- Partial errors of a response are available in the `errors` attribute of the lists returned by `get_items` and `get_browse_nodes`, and are reported in the message of `ItemsNotFoundError`
- `ErrorData` and `ResultList` available in `amazon_creatorsapi.models`
- `get_asin` and `errors` are available directly in `amazon_creatorsapi`
- The identifier that Amazon gives to a request is part of the message of the error, so it can be reported to Amazon support
- `close` method and context manager support in `AmazonCreatorsApi`, to release the connections of a client that is not going to be reused
- `py.typed` marker, so the type hints of the package are used by type checkers
- Migration guide from version 6, listing what can break in code written for `amazon_creatorsapi` and how to fix it
- The values accepted by `version`, the countries and the marketplace each one maps to, and the `marketplace` argument are documented, instead of having to read the code to find them
- `CONTRIBUTING.md`, with the setup of the project, the commands of the `Makefile`, the conventions of the code and the tests, and what a pull request is expected to carry
- Tests pinning the signatures of both clients and the hierarchy of the errors, so a change that breaks the code of the users is noticed

### Changed

- Requests time out after 30 seconds instead of waiting indefinitely, the refresh of the token included, which waited indefinitely in `AmazonCreatorsApi` and used the 5 second default of `httpx` in `AsyncAmazonCreatorsApi`. Pass `timeout=None` to restore the previous behaviour
- Errors are mapped from the response of the Creators API instead of the codes of the old Product Advertising API, so the reason and the fields that failed are part of the message
- A rejected request raises `InvalidArgumentError`, missing or expired credentials raise `AuthenticationError` and a forbidden request raises `AccessDeniedError`, instead of a generic `RequestError`
- Values rejected by the API constraints raise `InvalidArgumentError` instead of a `pydantic.ValidationError`
- Connection failures and unparseable responses raise `RequestError` instead of leaking the errors of the HTTP client
- An expired token is refreshed once and the request is sent again instead of failing
- `AuthenticationError` and `AccessDeniedError` are subclasses of `RequestError`, which is what a failed request raised before they got their own type
- `InvalidArgumentError` is also a `ValueError`, as the `pydantic.ValidationError` and the plain `ValueError` it replaced were
- `get_items` splits a request with more items than the API accepts into as many calls as needed, so any amount of items can be requested at once
- `get_items` returns the items in the order they were requested, and asks for duplicated items only once
- `get_items` raises `ItemsNotFoundError` when the response holds no requested item, as documented, instead of returning an empty list
- `search_items` rejects a search without any criteria instead of sending it to the API
- An unsupported `version` raises `InvalidArgumentError` instead of a plain `ValueError`, like the rest of the arguments of the clients, and a version of a family that the library cannot authenticate is rejected even when `auth_endpoint` is given, instead of being sent with the Cognito flow and rejected by Amazon without an explanation
- The error of an unsupported version tells that a newer version of a known family can be used by providing its `auth_endpoint`
- `AmazonCreatorsApi` validates the version when it is created, as `AsyncAmazonCreatorsApi` already did, instead of failing on the first request
- The auth flow of a version and the `Authorization` header it expects are decided in a single place shared by both clients, and the copies bundled in the SDK are pinned to them by tests, so a bump of the SDK cannot leave both halves disagreeing
- `AsyncAmazonCreatorsApi` builds its requests with the models of the SDK, so both clients validate the same values before sending a request
- Every client uses its own configuration for the SDK instead of the one shared by the whole process
- Throttling is measured with a monotonic clock and is safe to use from several threads
- `throttling` is validated like the rest of the options, so a negative or invalid value raises `InvalidArgumentError` instead of being accepted or failing with a `TypeError`
- The usage guide covers everything the README does, so the documentation does not have to be read in both places, and the README links to it
- The integration tests reach every operation of the API, feeds and reports included, and both clients share the same assertions, so a difference between them is a failure instead of a gap
- Every integration test reads the results of a single round of calls, which loads each request with as much as it can check, so the whole API is covered without spending more requests of the account
- The async integration tests make their calls when the suite runs instead of when the module is imported, so they are not sent when the tests are deselected and a failure is reported as such
- The CI workflow runs the test suite once per Python version instead of also running it inside the linter job, cancels superseded pull request runs and installs `uv` through a cached action
- The release workflow builds with `uv build`, and its check for an already existing tag looks for the tag name that is actually created, which never matched before
- Bumped the bundled `creatorsapi-python-sdk` from `1.2.0` to `1.3.0`, which makes `partnerTag` a required field of `SearchItemsRequestContent`
- Pinned `ruff` to the version run by pre-commit, so `make lint` matches CI

### Fixed

- Examples in the documentation that used names that do not exist, such as `SortBy.PRICE_LOW_TO_HIGH` or `GetItemsResource.ITEMINFO_TITLE`
- Documented limits of `item_count`, `min_reviews_rating` and `variation_page`, which did not match the ones accepted by the API
- A token response that does not hold JSON raises `AuthenticationError` in `AsyncAmazonCreatorsApi`, instead of the error of the JSON parser
- Errors reported by the transport, such as an invalid certificate, keep their reason instead of being reported as `Request failed with status 0`
- An ASIN longer than ten characters in a URL is rejected instead of being trimmed to a different item
- Threads sharing a client ask for a single token when the cached one expires, instead of one for every thread
- Search integration tests no longer assume Amazon always returns a full page of items

### Removed

- The deprecated `amazon_paapi` module and its bundled Product Advertising API 5.0 SDK, with `AmazonApi`, `amazon_paapi.errors`, `amazon_paapi.helpers`, `amazon_paapi.models` and `amazon_paapi.tools`. Use `amazon_creatorsapi` instead, following the [migration guide](https://python-amazon-paapi.readthedocs.io/en/latest/pages/migration-guide-6.html) for the credential, method and exception mapping
- Product Advertising API documentation and deprecation notices in the README and docs
- `API_KEY` and `API_SECRET` environment variables, only used by the removed module
- `six` dependency, which was not used

## [6.3.0] - 2026-05-15

### Added

- `delivery_flags` parameter in `search_items` for `amazon_creatorsapi` and `amazon_creatorsapi.aio`

## [6.2.0] - 2026-03-12

### Added

- LWA support in the `amazon_creatorsapi.aio` API layer

### Changed

- Bumped `creatorsapi-python-sdk` from `1.1.2` to `1.2.0`
- Updated bundled SDK support to include LWA endpoints for v3.x

## [6.1.0] - 2026-02-09

### Added

- Full async/await support with new `amazon_creatorsapi.aio` subpackage ([#143](https://github.com/sergioteula/python-amazon-paapi/pull/143))
- `AsyncAmazonCreatorsApi` class for non-blocking API interactions
- Async HTTP client with `httpx` integration for connection pooling
- `AuthenticationError` exception for improved OAuth2 error handling
- Optional `[async]` installation extra: `pip install python-amazon-paapi[async]`
- Comprehensive async test suite with integration tests
- Documentation for async API usage in README and usage guide
- `make docs` command in Makefile for building documentation

### Changed

- GitHub Actions workflow now installs async dependencies for complete test coverage
- Test coverage threshold lowered from 99% to 98% to accommodate async tests
- Additional Ruff linting rules for test files (ARG002, S101, S105, S106, SIM117)

## [6.0.0] - 2026-01-29

### Added

- New `amazon_creatorsapi` module for Amazon Creators API support
- `creatorsapi_python_sdk` package bundled for OAuth2 authentication
- `models` submodule exposing all SDK model classes (Item, Condition, SortBy, etc.)
- Migration guide from PAAPI to Creators API (`docs/pages/migration-guide-6.md`)
- Integration tests for the new Creators API module
- New dependencies: `pydantic>=2.0.0` and `requests>=2.28.0`

### Changed

- **BREAKING**: The `amazon_paapi` module is now deprecated in favor of `amazon_creatorsapi`
- Updated documentation to reflect the new Creators API module
- Reorganized utility functions into `amazon_creatorsapi.core` package
- Updated README with Creators API examples and deprecation notice

### Deprecated

- `amazon_paapi` module - use `amazon_creatorsapi` instead
- All PAAPI-specific documentation pages removed

### Removed

- Migration guides for versions 4 and 5 (`migration-guide-4.md`, `migration-guide-5.md`)

## [5.2.0] - 2026-01-11

### Added

- Support for OffersV2 resources with new model classes ([#141](https://github.com/sergioteula/python-amazon-paapi/pull/141))

## [5.1.0] - 2026-01-11

### Added

- Integration tests with real Amazon API calls
- Type hints throughout the codebase using `Literal` types for country codes
- `.env.template` file for easier development setup
- Code style guide for AI assistants (`.agent/rules/code-style-guide.md`)
- Pre-commit hooks with Ruff integration
- Version consistency check script (`scripts/check_version.py`)
- Manual release workflow (`release.yml`) that creates GitHub releases from CHANGELOG
- CI check to ensure CHANGELOG is updated in every PR

### Changed

- **BREAKING**: Minimum Python version raised from 3.7 to 3.9
- Migrated from `setup.py` to `pyproject.toml` for project configuration
- Replaced multiple linters (Flake8, isort, Black, Pylint) with Ruff
- Replaced Docker-based development environment with `uv` package manager
- Consolidated coverage, mypy, and pytest configuration into `pyproject.toml`
- Renamed test files to use `_test.py` suffix instead of `test_` prefix
- Updated GitHub Actions workflows to use `uv` instead of Docker
- Improved docstrings across the codebase
- Completely rewritten README with clearer structure and examples
- Updated Read the Docs configuration to v2 format with modern Sphinx versions
- Updated documentation to furo theme

### Removed

- `setup.py` - replaced by `pyproject.toml`
- `.coveragerc` - configuration moved to `pyproject.toml`
- `.flake8` - replaced by Ruff configuration in `pyproject.toml`
- Docker development environment (`docker/`, `docker-compose.yml`)
- Legacy shell scripts (`scripts/` directory)
- Custom git hooks (`.githooks/`) - replaced by pre-commit
