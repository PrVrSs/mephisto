SHELL := /usr/bin/env bash

.PHONY: unit
unit:
	poetry run pytest -v \
		-vv \
		--cov=mephisto \
		--capture=no \
		--cov-report=term-missing \
		--cov-config=.coveragerc \

.PHONY: mypy
mypy:
	poetry run mypy mephisto

.PHONY: lint
lint:
	poetry run pylint mephisto


test: lint mypy unit
