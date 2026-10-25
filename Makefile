PYTHON ?= .venv/bin/python
ARGS ?= config.json

.PHONY: install run debug lint clean

install:
	uv sync --group dev

run:
	$(PYTHON) pac-man.py $(ARGS)

debug:
	$(PYTHON) -m pdb pac-man.py $(ARGS)

lint:
	.venv/bin/flake8 .
	.venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('src').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in map(pathlib.Path, ('__pycache__', '.mypy_cache', '.pytest_cache', '.ruff_cache', 'build'))]"
