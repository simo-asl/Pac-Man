# Pac-Man

A Python project using Pygame and the 42 MazeGenerator package. The app lives
directly in `src/main.py` and opens a generated maze preview.

## Setup

Install [uv](https://docs.astral.sh/uv/), then run:

```sh
uv sync
uv run python src/main.py
```

Python 3.12 is selected by `.python-version`. The project supports Python 3.12
and 3.13; Pygame 2.6.1 does not provide a Python 3.14 wheel.

## MazeGenerator dependency

The supplied [MazeGenerator archive](https://cdn.intra.42.fr/document/document/55104/mazegenerator-00001.zip)
contains a wheel rather than an installable source archive. Its extracted
`mazegenerator-2.1.0-py3-none-any.whl` is stored under `vendor/` and declared
as a local `uv` source in `pyproject.toml`, so `uv sync` can install it without
downloading the original ZIP again. The download itself is ignored by Git.

Close the preview window or press Escape to exit.
