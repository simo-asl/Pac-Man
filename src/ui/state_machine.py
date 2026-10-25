"""Export the public state_machine package interface."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ..game_controller import GameController
from .menu import Menu
from .state import GameState


class StateMachine:
    """Dispatch keyboard events and rendering to the active screen."""

    def __init__(self, menu: Menu, game: GameController) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            menu: Menu handler used for navigation and highscore entry.
            game: Current game controller or gameplay state.

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
        """Select the screen to process on the next frame.

        Args:
            new_state: Screen state to activate.

        Returns:
            None.
        """
        self.state = new_state

    def run_state(self, keys: list[pygame.event.Event]) -> None:
        """Pass input and drawing to the current screen.

        Args:
            keys: Keyboard events collected for the current frame.

        Returns:
            None.
        """
        scene = self.objects[self.state]
        scene.run(self.state, keys)
