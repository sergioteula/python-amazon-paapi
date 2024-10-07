export UID:=$(shell id -u)
export GID:=$(shell id -g)

export PYTHON_TAGS = 3.7 3.8 3.9 3.10 3.11 3.12

setup:
	@git config --unset-all core.hooksPath || true
	@git config --local core.hooksPath .githooks

build:
	@docker build --build-arg TAG="3.12" --build-arg UID="${UID}" --build-arg GID="${GID}" -t python-amazon-paapi .

test: build
	@docker run --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m unittest"

test-all-python-tags:
	@for tag in $$PYTHON_TAGS; do \
		docker build --build-arg TAG="$$tag" --build-arg UID="${UID}" --build-arg GID="${GID}" -t python-amazon-paapi .; \
		docker run --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m unittest"; \
	done

lint: build
	@docker run --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m pre_commit run -a"

pre-commit:
	@./.githooks/pre-commit
