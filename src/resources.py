"""Resolve bundled resources independently of the working directory."""

from pathlib import Path


def resource_path(path: str) -> Path:
    """Return an absolute path in the source tree or PyInstaller bundle.

    Args:
        path: Project-relative resource filename.

    Returns:
        Path: Absolute path in the source tree or executable bundle.
    """
    return Path(__file__).resolve().parent.parent / path
