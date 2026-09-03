# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.2.0] - 2026-09-03

### Added

- `get_items` splits a request with more items than the API accepts into as many calls as needed, so any amount of items can be requested at once
- `include_unavailable` parameter in `get_items` to get an item holding only the ASIN for every requested item missing from the response
- Partial errors of a response are available in the `errors` attribute of the lists returned by `get_items` and `get_browse_nodes`, and are reported in the message of `ItemsNotFoundError`
- `ErrorData` and `ResultList` available in `amazon_creatorsapi.models`

### Changed

- `get_items` returns the items in the order they were requested, and asks for duplicated items only once
- `AmazonCreatorsApi` applies the timeout to the OAuth2 token refresh as well, which previously waited indefinitely, and reports its failures as `AuthenticationError`
- `AmazonCreatorsApi` validates the version when it is created, as `AsyncAmazonCreatorsApi` already did, instead of failing on the first request
- Values rejected by the API constraints raise `InvalidArgumentError` instead of a `pydantic.ValidationError`
- `get_items` raises `ItemsNotFoundError` when the response holds no items, as documented, instead of returning an empty list

## [7.1.0] - 2026-09-03

### Added

- `timeout` parameter in `AmazonCreatorsApi` and `AsyncAmazonCreatorsApi` to set the request timeout in seconds, or `None` to wait indefinitely

### Changed

- `AmazonCreatorsApi` API requests now time out after 30 seconds instead of waiting indefinitely, matching the timeout already used by `AsyncAmazonCreatorsApi`. Pass `timeout=None` to restore the previous behavior
- `AsyncAmazonCreatorsApi` now applies `timeout` to the OAuth2 token refresh as well, which previously always used the 5 second default from `httpx`

## [7.0.0] - 2026-09-03

### Removed

- The deprecated `amazon_paapi` module and its bundled Product Advertising API 5.0 SDK
- `AmazonApi`, `amazon_paapi.errors`, `amazon_paapi.helpers`, `amazon_paapi.models` and `amazon_paapi.tools`
- Product Advertising API documentation and deprecation notices in the README and docs
- `API_KEY` and `API_SECRET` environment variables, only used by the removed module

### Changed

- Use `amazon_creatorsapi` instead. See the
  [migration guide](https://python-amazon-paapi.readthedocs.io/en/latest/pages/migration-guide-6.html)
  for the credential, method and exception mapping

## [6.4.0] - 2026-09-03

### Added

- `list_feeds`, `get_feed`, `list_reports` and `get_report` methods in `amazon_creatorsapi` and `amazon_creatorsapi.aio`
- `Feed`, `FeedType`, `ReportMetadata` and `ReportType` in `amazon_creatorsapi.models`
- `FeedType` and `ReportType` models in the bundled SDK
- `feedType` field in `Feed` and `GetFeedRequestContent` models
- `reportType` field in `ReportMetadata` and `GetReportRequestContent` models

### Changed

- Bumped `creatorsapi-python-sdk` from `1.2.0` to `1.3.0`
- `partnerTag` is now a required field in `SearchItemsRequestContent`
- Pinned `ruff` to the version run by pre-commit, so `make lint` matches CI

### Fixed

- Search integration tests no longer assume Amazon always returns a full page of items

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
