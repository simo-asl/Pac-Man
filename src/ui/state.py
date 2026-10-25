"""Enumerate application screens."""

from enum import Enum, auto


class GameState(Enum):
    """Enumerate the application screens."""

    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    GAME_OVER = auto()
    NAME_INPUT = auto()
    LEVEL_COMPLETE = auto()
    VICTORY = auto()
