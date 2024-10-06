export UID:=$(shell id -u)
export GID:=$(shell id -g)

setup:
	@git config --unset-all core.hooksPath || true
	@git config --local core.hooksPath .githooks

build:
	@docker build --build-arg TAG="3.12" --build-arg UID="${UID}" --build-arg GID="${GID}" -t python-amazon-paapi .

test: build
	@docker run --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m unittest"

lint: build
	@docker run --rm -u "${UID}:${GID}" -v "${PWD}:/code" python-amazon-paapi -c "python -m pre_commit run -a"

pre-commit:
	@./.githooks/pre-commit
