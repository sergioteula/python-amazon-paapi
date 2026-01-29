export UID:=$(shell id -u)
export GID:=$(shell id -g)

export PYTHON_TAGS = 3.9 3.10 3.11 3.12 3.13 3.14

setup:
	@uv run pre-commit install

test:
	@touch .env
	@uv run --env-file .env pytest -rs

coverage:
	@uv run pytest -rs --cov=amazon_paapi --cov=amazon_creatorsapi --cov-report=html --cov-report=term --cov-report=xml

test-all-python-tags:
	@touch .env
	@for tag in $$PYTHON_TAGS; do \
		uv run --env-file .env --python "$$tag" pytest -rs --no-cov; \
	done

lint:
	@uv run ruff check --fix .

format:
	@uv run ruff format .

mypy:
	@uv run mypy .

pre-commit:
	@uv run pre-commit run -a
