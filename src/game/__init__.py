"""Manage scoring, collisions, level timing and pauses."""

from .game import Game
from .highscore import score
from .player import Player

__all__ = ["Game", "Player", "score"]
