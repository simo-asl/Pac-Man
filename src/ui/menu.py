"""Handle menu navigation, name entry, and highscore submission."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..game.highscore import High, score
from .draw import Draw
from .menu_view import MenuView
from .state import GameState

if TYPE_CHECKING:
    from .state_machine import StateMachine


class Menu:
    """Own menu state and input while MenuView owns page rendering."""

    def __init__(self, drawer: Draw) -> None:
        """Initialize menu selection, form state, and its drawing view.

        Args:
            drawer: Drawing helper shared by all menu screens.

        Returns:
            None.
        """
        self.view = MenuView(drawer)
        self.options = ['START GAME', 'HIGHSCORES', 'INSTRUCTIONS', 'EXIT']
        self.selected_index = 0
        self.player_name = ''
        self.error_message = ''
        self.machine: StateMachine | None = None
        self.highscore_store = High('highscores.json')
        self.high_scores: list[score] = []

    def set_machine(self, state_machine: StateMachine) -> None:
        """Connect navigation and load scores from the configured file.

        Args:
            state_machine: Coordinator owning the active game configuration.

        Returns:
            None.
        """
        self.machine = state_machine
        self.highscore_store = High(
            state_machine.game.config.highscore_filename
        )
        self.high_scores = self.highscore_store.get_top_scores()

    def _handle_main_menu_key(self, key: int) -> None:
        """Move the selection or activate the chosen main-menu action.

        Args:
            key: Pygame key code from a key-down event.

        Returns:
            None.
        """
        if key in (pygame.K_UP, pygame.K_DOWN):
            selection_step = -1 if key == pygame.K_UP else 1
            self.selected_index = (
                self.selected_index + selection_step
            ) % len(self.options)
        elif key == pygame.K_RETURN:
            self._activate_selection()

    def _activate_selection(self) -> None:
        """Execute the selected action using the connected state machine.

        Returns:
            None.
        """
        if self.machine is None:
            return
        selected_action = self.options[self.selected_index]
        if selected_action == 'START GAME':
            self.error_message = ''
            self.machine.game.start_game()
        elif selected_action == 'HIGHSCORES':
            self.high_scores = self.highscore_store.get_top_scores()
            self.machine.change_state(GameState.HIGHSCORES)
        elif selected_action == 'INSTRUCTIONS':
            self.machine.change_state(GameState.INSTRUCTIONS)
        elif selected_action == 'EXIT':
            self.machine.running = False

    def _handle_name_input_key(self, event: pygame.event.Event) -> None:
        """Edit the name field or submit its contents.

        Args:
            event: Key-down event containing a key code and typed text.

        Returns:
            None.
        """
        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.error_message = ''
        elif event.key == pygame.K_RETURN:
            self._submit_score()
        else:
            typed_character = event.unicode
            is_ascii = typed_character.isascii()
            is_allowed = typed_character.isalnum() or typed_character == ' '
            name_has_room = len(self.player_name) < 10
            if typed_character and is_ascii and is_allowed and name_has_room:
                self.player_name += typed_character
                self.error_message = ''

    def _submit_score(self) -> None:
        """Validate and save the name form before returning to the menu.

        Returns:
            None. Validation and file failures stay on the current form.
        """
        if self.machine is None:
            return
        if not self.highscore_store.valid_name(self.player_name):
            self.error_message = 'Enter 1-10 letters, numbers or spaces.'
            return
        final_score = self.machine.game.game.score
        if not self.highscore_store.add_score(self.player_name, final_score):
            self.error_message = 'Cannot save score. Check the file and retry.'
            return
        self.high_scores = self.highscore_store.get_top_scores()
        self.error_message = ''
        self.machine.change_state(GameState.MENU)

    def handle_keys(self, state: GameState, event: pygame.event.Event) -> None:
        """Route one keyboard event to the active menu action.

        Args:
            state: Menu page receiving the event.
            event: Pygame input event; events other than key-down are ignored.

        Returns:
            None.
        """
        if event.type != pygame.KEYDOWN or self.machine is None:
            return
        if state == GameState.MENU:
            self._handle_main_menu_key(event.key)
        elif state == GameState.NAME_INPUT:
            self._handle_name_input_key(event)
        elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            if state == GameState.VICTORY:
                self.begin_name_input()
            elif state in (GameState.HIGHSCORES, GameState.INSTRUCTIONS):
                self.machine.change_state(GameState.MENU)

    def begin_name_input(self) -> None:
        """Clear the name form when a game finishes.

        Returns:
            None.
        """
        self.player_name = ''
        self.error_message = ''
        if self.machine is not None:
            self.machine.change_state(GameState.NAME_INPUT)

    def _render(self, state: GameState) -> None:
        """Select the view method for the current menu page.

        Args:
            state: Menu page to render without changing game state.

        Returns:
            None.
        """
        if state == GameState.MENU:
            self.view.draw_menu(
                self.options, self.selected_index, self.error_message,
            )
        elif state == GameState.HIGHSCORES:
            self.view.draw_highscore(self.high_scores)
        elif state == GameState.INSTRUCTIONS:
            self.view.draw_instructions()
        elif self.machine is not None:
            final_score = self.machine.game.game.score
            if state == GameState.VICTORY:
                self.view.draw_victory(final_score)
            elif state == GameState.NAME_INPUT:
                self.view.draw_name_input(
                    final_score, self.player_name, self.error_message,
                )

    def run(self, state: GameState, events: list[pygame.event.Event]) -> None:
        """Run a menu frame, stopping when an input changes the screen.

        Args:
            state: Menu page active at the start of the frame.
            events: Input events collected for this frame.

        Returns:
            None.
        """
        for event in events:
            self.handle_keys(state, event)
            if self.machine is not None and self.machine.state != state:
                return
        self._render(state)
