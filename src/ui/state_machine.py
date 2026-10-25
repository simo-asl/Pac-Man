"""Dispatch each frame to the active scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ..game_controller import GameController
from .menu import Menu
from .state import GameState


class StateMachine:
    """Route each frame to the current screen."""

    def __init__(self, menu: Menu, game: GameController) -> None:
        """Initialize this object and its dependencies.

        Args:
            menu: Menu scene used for navigation and score entry.
            game: Active game state, score and timing information.

        Returns:
            None.
        """
        self.menu = menu
        self.game = game
        self.state = GameState.MENU
        self.objects: dict[GameState, Menu | GameController] = {
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
        """Select the next screen.

        Args:
            new_state: Screen to activate next.

        Returns:
            None.
        """
        self.state = new_state

    def run_state(self, keys: list[pygame.event.Event]) -> None:
        """Dispatch the current frame to the active screen.

        Args:
            keys: Keyboard events collected for this frame.

        Returns:
            None.
        """
        scene = self.objects[self.state]
        scene.run(self.state, keys)
