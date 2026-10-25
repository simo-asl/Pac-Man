"""Locate bundled resources in source checkouts and installed packages."""

from pathlib import Path


def resource_path(path: str) -> Path:
    """Resolve a project-relative resource filename.

    Args:
        path: Project-relative resource filename.

    Returns:
        Absolute resource path inside the installed application package.
    """
    relative = Path(path)
    if relative.parts and relative.parts[0] == 'src':
        relative = Path(*relative.parts[1:])
    return Path(__file__).resolve().parent / relative
