from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    GAME_OVER = auto()
    NAME_INPUT = auto()
    LEVEL_COMPLETE = auto()
