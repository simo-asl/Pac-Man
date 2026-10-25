"""Define menu and gameplay screen states."""

from enum import Enum, auto


class GameState(Enum):
    """Enumerate every menu, gameplay and result screen.
    """
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    GAME_OVER = auto()
    NAME_INPUT = auto()
    LEVEL_COMPLETE = auto()
    VICTORY = auto()
