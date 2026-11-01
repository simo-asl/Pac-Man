"""Provide elapsed gameplay time independent from Pygame initialization."""

from time import monotonic


def now_ms() -> int:
    """Return a monotonic timestamp in milliseconds for gameplay timers."""
    return int(monotonic() * 1000)
