PYTHON := .venv/bin/python
ARGS ?= config.json
UV_ENV := UV_PROJECT_ENVIRONMENT=$(CURDIR)/.venv VIRTUAL_ENV=

.DEFAULT_GOAL := run

.PHONY: install run debug lint lint-strict clean

install:
	$(UV_ENV) uv sync --group dev
	$(PYTHON) -c "import pygame, mazegenerator, hjson, pydantic, bdfparser, flake8, mypy; print('All project dependencies are installed.')"

run:
	$(PYTHON) pac-man.py $(ARGS)

debug:
	$(PYTHON) -m pdb pac-man.py $(ARGS)

lint:
	.venv/bin/flake8 .
	.venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache -o -name .ruff_cache \) -not -path './.venv/*' -prune -exec rm -rf {} +
	@rm -rf build
