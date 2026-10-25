"""Locate bundled resources in source checkouts and installed packages."""

from pathlib import Path


def resource_path(path: str) -> Path:
    """Resolve a project-relative resource filename.

    Args:
        path: Project-relative resource filename.

    Returns:
        Absolute resource path inside the installed application package.
    """
    package_directory = Path(__file__).resolve().parent
    return package_directory / path
