from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_controller import GameController
from .menu import Menu
from .state import GameState


class StateMachine:
    def __init__(self, menu: Menu, game: GameController):
        self.menu = menu
        self.game = game
        self.state = GameState.MENU
        self.objects = {
            GameState.HIGHSCORES: self.menu,
            GameState.PLAYING: self.game,
            GameState.PAUSED: self.game,
            GameState.INSTRUCTIONS: self.menu,
            GameState.GAME_OVER: self.game,
            GameState.NAME_INPUT: self.menu,
            GameState.LEVEL_COMPLETE: self.game,
            GameState.VICTORY: self.menu,
            GameState.MENU: self.menu,
        }
        self.running = True

    def change_state(self, new_state: GameState) -> None:
        self.state = new_state

    def run_state(self, keys, **kwargs):
        scene = self.objects[self.state]
        scene.run(self.state, keys, **kwargs)
