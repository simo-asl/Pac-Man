"""Menu navigation and score entry; visual layouts live in menu_view.py."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..game.highscore import High
from .draw import Draw
from .menu_view import MenuView
from .state import GameState

if TYPE_CHECKING:
    from ..game.highscore import score
    from .state_machine import StateMachine


class Menu:
    """Handle keyboard navigation and saving without owning page layouts."""

    def __init__(self, draw: Draw) -> None:
        """Keep existing menu state and prepare its drawing companion.

        Args:
            draw: Drawing helper for the target surface.

        Returns:
            None.
        """
        self.draw = draw
        self.view = MenuView(draw)
        self.selected = 0
        self.options = ["START GAME", "HIGHSCORES", "INSTRUCTIONS", "EXIT"]
        self.machine: StateMachine | None = None
        self.player_name = ""
        self.name_error = ""
        self.score_saved = False

    def move_selection(self, direction: int) -> None:
        """Move the highlighted menu option, wrapping at the ends.

        Args:
            direction: Selection offset, normally -1 or 1.

        Returns:
            None.
        """
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        """Return the currently highlighted option.

        Returns:
            str: Label of the currently highlighted main-menu option.
        """
        return self.options[self.selected]

    def draw_menu(self) -> None:
        """Render the main menu using the current selection and error.

        Returns:
            None.
        """
        self.view.main(self.options, self.selected, self.name_error)

    def draw_highscore(self, scores: list[score]) -> None:
        """Render the supplied top-ten list.

        Args:
            scores: Ranked saved entries to display, limited to the top ten.

        Returns:
            None.
        """
        self.view.highscores(scores)

    def set_machine(self, state_machine: StateMachine) -> None:
        """Connect this screen to the application state machine.

        Args:
            state_machine: Application state machine connected to this scene.

        Returns:
            None.
        """
        self.machine = state_machine

    def handle_keys(
        self,
        state: GameState,
        event: pygame.event.Event,
    ) -> None:
        """Handle a keyboard event for the current screen.

        Args:
            state: Screen currently handling input and rendering.
            event: Pygame keyboard event to process.

        Returns:
            None.
        """
        if event.type != pygame.KEYDOWN:
            return
        if self.machine is None:
            return
        match state:
            case GameState.MENU:
                if event.key == pygame.K_UP:
                    self.move_selection(-1)

                elif event.key == pygame.K_DOWN:
                    self.move_selection(1)

                elif event.key == pygame.K_RETURN:
                    selected = self.select()

                    if selected == "START GAME":
                        self.player_name = ""
                        self.name_error = ""
                        self.score_saved = False
                        self.machine.game.start_game()

                    elif selected == "HIGHSCORES":
                        self.machine.change_state(GameState.HIGHSCORES)

                    elif selected == "INSTRUCTIONS":
                        self.machine.change_state(GameState.INSTRUCTIONS)

                    elif selected == "EXIT":
                        self.machine.running = False

            case GameState.HIGHSCORES | GameState.INSTRUCTIONS:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.machine.change_state(GameState.MENU)

            case GameState.NAME_INPUT:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    name = self.player_name.strip()
                    if not name:
                        self.name_error = "Please enter a name."
                    elif not self.score_saved:
                        high = High(
                            self.machine.game.config.highscore_filename
                        )
                        if high.add_score(name, self.machine.game.game.score):
                            self.score_saved = True
                            self.name_error = ""
                            self.machine.change_state(GameState.MENU)
                        else:
                            self.name_error = (
                                "Could not save score. Press Enter to retry."
                            )

                elif (
                    event.unicode.isascii()
                    and (event.unicode.isalnum() or event.unicode == " ")
                    and len(self.player_name) < 10
                ):
                    self.player_name += event.unicode
                    self.name_error = ""

            case GameState.VICTORY:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.machine.change_state(GameState.NAME_INPUT)

    def run(self, state: GameState, keys: list[pygame.event.Event]) -> None:
        """Handle input before drawing the active menu page.

        Args:
            state: Screen currently handling input and rendering.
            keys: Keyboard events collected for this frame.

        Returns:
            None.
        """
        if self.machine is None:
            return
        for event in keys:
            self.handle_keys(state, event)
            if self.machine.state != state:
                return
        match state:
            case GameState.MENU:
                self.draw_menu()
            case GameState.HIGHSCORES:
                high = High(self.machine.game.config.highscore_filename)
                self.draw_highscore(high.get_top_scores())
            case GameState.INSTRUCTIONS:
                self.view.instructions()
            case GameState.VICTORY:
                self.view.victory(self.machine.game.game.score)
            case GameState.NAME_INPUT:
                self.view.name_input(
                    self.machine.game.game.score,
                    self.player_name,
                    self.name_error,
                )
