export UID:=$(shell id -u)
export GID:=$(shell id -g)

export PYTHON_TAGS = 3.8 3.9 3.10 3.11 3.12 3.13 3.14 3.15

setup:
	@uv run pre-commit install

test:
	@touch .env
	@uv run --env-file .env pytest -rs

coverage:
	@uv run pytest -rs --cov=amazon_paapi --cov-report=html --cov-report=term --cov-report=xml

test-all-python-tags:
	@touch .env
	@for tag in $$PYTHON_TAGS; do \
		uv run --env-file .env --python "$$tag" pytest -rs --no-cov; \
	done

lint:
	@uv run ruff check --fix .

mypy:
	@uv run mypy .

pre-commit:
	@uv run pre-commit run -a
