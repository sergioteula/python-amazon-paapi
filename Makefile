export UID:=$(shell id -u)
export GID:=$(shell id -g)

export PYTHON_TAGS = 3.7 3.8 3.9 3.10 3.11 3.12

setup:
	@git config --unset-all core.hooksPath || true
	@git config --local core.hooksPath .githooks

build:
	@docker build --build-arg TAG="3.12" --build-arg UID="${UID}" --build-arg GID="${GID}" -t python-amazon-paapi .

coverage: build
	@touch .env
	@docker run -t --rm -u "${UID}:${GID}" -v "${PWD}:/code" --env-file .env python-amazon-paapi -c \
		"python -m coverage run -m pytest -rs && python -m coverage xml && python -m coverage report"

test: build
	@touch .env
	@docker run -t --rm -u "${UID}:${GID}" -v "${PWD}:/code" --env-file .env python-amazon-paapi -c "python -m pytest -rs"

test-all-python-tags:
	@touch .env
	@for tag in $$PYTHON_TAGS; do \
		docker build --build-arg TAG="$$tag" --build-arg UID="${UID}" --build-arg GID="${GID}" -t python-amazon-paapi .; \
		docker run -t --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m pytest -rs"; \
	done

lint: build
	@touch .env
	@docker run --rm -t -u "${UID}:${GID}" -v "${PWD}:/code" --env-file .env python-amazon-paapi -c "python -m pre_commit run -a"

pre-commit:
	@./.githooks/pre-commit
