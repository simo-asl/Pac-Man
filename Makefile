PYTHON = .venv/bin/python
ARGS ?= config.json

.PHONY: install run debug clean lint package

install:
	uv sync

run:
	$(PYTHON) pac-man.py $(ARGS)

debug:
	$(PYTHON) -m pdb pac-man.py $(ARGS)

lint:
	.venv/bin/flake8 .
	.venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	.venv/bin/pyinstaller --noconfirm pac-man.spec
	$(PYTHON) package.py

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('src').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in ('__pycache__', '.mypy_cache', '.pytest_cache', '.ruff_cache', 'build')]"
