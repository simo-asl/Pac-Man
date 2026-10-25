"""Route frames to the handler registered for the active screen."""

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
        """Connect the menu and game handlers and select the main menu.

        Args:
            menu: Menu handler used for navigation and highscore entry.
            game: Current game controller or gameplay state.

        Returns:
            None.
        """
        self.menu = menu
        self.game = game
        self.state = GameState.MENU
        self.running = True

    def change_state(self, new_state: GameState) -> None:
        """Select the screen to process on the next frame.

        Args:
            new_state: Screen state to activate.

        Returns:
            None.
        """
        self.state = new_state

    def run_state(self, events: list[pygame.event.Event]) -> None:
        """Pass input and drawing to the current screen.

        Args:
            events: Input events collected for the current frame.

        Returns:
            None. A failed screen reports its error and returns to the menu.

        Raises:
            RuntimeError: The main menu itself cannot run or draw.
        """
        game_screens = (
            GameState.PLAYING,
            GameState.PAUSED,
            GameState.GAME_OVER,
            GameState.LEVEL_COMPLETE,
        )
        try:
            if self.state in game_screens:
                self.game.run(self.state, events)
            else:
                self.menu.run(self.state, events)
        except Exception as error:
            message = f'{self.state.name} screen failed: {error}'
            if self.state == GameState.MENU:
                raise RuntimeError(message) from None
            print(f'Pac-Man: {message}')
            self.menu.error_message = message
            self.change_state(GameState.MENU)
