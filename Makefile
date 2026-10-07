PYTHON = python3
SRC = src


.PHONY: install run clean lint

install:
	uv sync

run:
	uv run $(PYTHON) -m $(SRC) $(ARGS)

lint:
	uv run flake8 $(SRC)
	uv run mypy $(SRC)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
