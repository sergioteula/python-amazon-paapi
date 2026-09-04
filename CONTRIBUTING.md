# Contributing

Thanks for taking the time to contribute. This guide covers how to set the project up,
what the checks expect and how a change should be shaped.

## Setting up

The project is managed with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/sergioteula/python-amazon-paapi.git
cd python-amazon-paapi
uv sync --extra async
make setup
```

`make setup` installs the pre-commit hooks, which run Ruff, mypy and the tests before
every commit. The `async` extra is needed to run the tests of `AsyncAmazonCreatorsApi`.

Copy `.env.template` to `.env` and fill it with your Creators API credentials to run the
integration tests. Without it the unit tests still run, and the integration tests are
skipped and reported as such.

## Commands

| Command                     | What it does                                            |
| --------------------------- | ------------------------------------------------------- |
| `make test`                 | Run the test suite                                      |
| `make coverage`             | Run the tests with a coverage report                    |
| `make test-all-python-tags` | Run the tests on every supported Python version         |
| `make lint`                 | Run Ruff and apply the fixes it can make                |
| `make format`               | Format the code with Ruff                               |
| `make mypy`                 | Check the types                                         |
| `make pre-commit`           | Run every hook against all the files, as CI does        |
| `make docs`                 | Build the documentation into `docs/_build/html`          |

## Layout

| Path                      | What it holds                                                     |
| ------------------------- | ------------------------------------------------------------------ |
| `amazon_creatorsapi/`     | The library: the clients, the errors and the core utilities        |
| `creatorsapi_python_sdk/` | The SDK generated from the API schema, vendored and not edited     |
| `tests/`                  | The test suite, mirroring the structure of `amazon_creatorsapi`    |
| `docs/`                   | The Sphinx documentation published on Read the Docs                |

`creatorsapi_python_sdk` is generated code: it is excluded from Ruff, mypy and the
formatter, and it is replaced wholesale when the SDK is bumped, so a fix belongs in
`amazon_creatorsapi` and not there.

## Style

- Everything in English: code, comments, docstrings and commit messages.
- Docstrings on every function, and type hints on every signature.
- Comments only where the reason for the code is not obvious from the code itself.
- No abbreviations or single-letter names.
- `noqa` only when there is no other way, and never without a reason.

## Tests

- Tests come with the change, following TDD.
- The `tests` directory mirrors the structure of `amazon_creatorsapi`.
- `unittest.TestCase` with `setUp` and `tearDown`, unittest assertions and `@patch`
  decorators rather than context managers.
- Coverage may not drop below 98%, which is enforced by the test run.

## Documentation

A change that adds or changes something a user can see belongs in the documentation as
well:

- `README.md` and `docs/pages/usage-guide.md` cover the same ground, the guide in more
  depth. Keep both in step.
- Docstrings feed the API reference, so a new argument is documented there too.

## Sending a change

1. Add an entry to `CHANGELOG.md`, under `[Unreleased]`, in the section that matches the
   change: `Added`, `Changed`, `Fixed` or `Removed`. CI rejects a pull request that does
   not touch the changelog.
2. Run `make pre-commit` and make sure everything passes.
3. Open the pull request describing what changes for the user and why.

The version lives in `pyproject.toml`, `docs/conf.py` and `CHANGELOG.md`, and
`scripts/check_version.py` checks that the three agree. Only a release changes them.

## Getting help

Ask in the [Telegram group](https://t.me/PythonAmazonPAAPI) or open an
[issue](https://github.com/sergioteula/python-amazon-paapi/issues).
