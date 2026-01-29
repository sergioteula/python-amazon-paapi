# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
