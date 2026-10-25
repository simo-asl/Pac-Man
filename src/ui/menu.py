"""Keyboard-driven menu, instructions, results and highscore entry."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..game.highscore import High, score
from .content import INSTRUCTIONS
from .draw import Draw
from .state import GameState

if TYPE_CHECKING:
    from .state_machine import StateMachine

GOLD = (255, 220, 50)
TEXT = (240, 240, 240)
MUTED = (180, 190, 210)
ERROR = (255, 110, 110)


class Menu:
    """Keep navigation and score saving in one menu state handler."""

    def __init__(self, draw: Draw) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            draw: Drawing helper used to prepare or display game images.

        Returns:
            None.
        """
        self.draw = draw
        self.width, self.height = draw.screen.get_size()
        self.size = max(18, self.height // 32)
        self.selected = 0
        self.options = ['START GAME', 'HIGHSCORES', 'INSTRUCTIONS', 'EXIT']
        self.player_name = ''
        self.name_error = ''
        self.machine: StateMachine | None = None
        self.images = {}
        for state, filename in (
            (GameState.MENU, 'main_menu.png'),
            (GameState.HIGHSCORES, 'highscores.png'),
            (GameState.INSTRUCTIONS, 'instructions.png'),
            (GameState.VICTORY, 'victory_image.png'),
            (GameState.NAME_INPUT, 'name_input.png'),
        ):
            image = draw.load_image(
                f'src/game/assets/better_backgrounds/{filename}'
            )
            self.images[state] = draw.scale_image(
                image, (self.width, self.height)
            )
        self.high = High('highscores.json')
        self.scores: list[score] = []

    def set_machine(self, state_machine: StateMachine) -> None:
        """Attach the state machine used for screen transitions.

        Args:
            state_machine: State machine coordinating menu and gameplay
                screens.

        Returns:
            None.
        """
        self.machine = state_machine
        self.high = High(state_machine.game.config.highscore_filename)
        self.scores = self.high.get_top_scores()

    def move_selection(self, direction: int) -> None:
        """Wrap keyboard selection around the available choices.

        Args:
            direction: Signed number of menu options to move by.

        Returns:
            None.
        """
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        """Return the currently selected action.

        Returns:
            Label of the currently selected main-menu option.
        """
        return self.options[self.selected]

    def line(
        self, text: str, row: float, color: tuple[int, int, int] = TEXT,
        large: bool = False,
    ) -> None:
        """Place centered text inside the artwork's clear middle area.

        Args:
            text: Text to measure or render.
            row: Vertical position as a fraction of the window height.
            color: RGB color for the pixels, outline or text.
            large: Whether to use the larger heading font size.

        Returns:
            None.
        """
        self.draw.draw_text(
            text, self.width // 2, int(self.height * row),
            self.size * 2 if large else self.size, color, True,
            max_width=self.width * 3 // 5,
        )

    def page(self, state: GameState, title: str, hint: str) -> None:
        """Frame content with the original artwork and a readable panel.

        Args:
            state: Screen state whose input or content is being processed.
            title: Heading shown at the top of the screen or panel.
            hint: Keyboard guidance shown at the bottom of the page.

        Returns:
            None.
        """
        self.draw.draw_image(self.images[state], 0, 0)
        self.draw.fill_rect(
            self.width // 5, self.height // 10,
            self.width * 3 // 5, self.height * 4 // 5, (8, 12, 22),
        )
        self.draw.draw_rect(
            self.width // 5, self.height // 10,
            self.width * 3 // 5, self.height * 4 // 5, GOLD, 2,
        )
        self.line(title, .15, GOLD, True)
        self.line(hint, .83, MUTED)

    def draw_menu(self) -> None:
        """Show all four required main-menu actions.

        Returns:
            None.
        """
        self.page(
            GameState.MENU, 'PAC-MAN', 'UP / DOWN SELECT   ENTER CONFIRM'
        )
        for index, option in enumerate(self.options):
            self.line(
                ('> ' if index == self.selected else '') + option,
                .34 + index * .1, GOLD if index == self.selected else TEXT,
            )
        if self.name_error:
            self.line(self.name_error, .76, ERROR)

    def draw_highscore(self, scores: list[score]) -> None:
        """Fit all ten entries, with separate columns for names and scores.

        Args:
            scores: Ranked highscore entries to display, limited to ten.

        Returns:
            None.
        """
        self.page(GameState.HIGHSCORES, 'HIGH SCORES', 'ENTER / ESC BACK')
        if not scores:
            self.line('No scores yet. Start your first game!', .46)
        for index, entry in enumerate(scores[:10]):
            y = int(self.height * (.28 + index * .048))
            self.draw.draw_text(
                f'{index + 1:2}.  {entry.name}', self.width * 6 // 25,
                y, self.size, GOLD if index == 0 else TEXT,
                max_width=self.width * 3 // 10,
            )
            self.draw.draw_text(
                str(entry.score), self.width * 17 // 25, y,
                self.size, TEXT, True, max_width=self.width // 7,
            )

    def handle_keys(self, state: GameState, event: pygame.event.Event) -> None:
        """Apply keyboard events to the current screen state.

        Args:
            state: Screen state whose input or content is being processed.
            event: Pygame keyboard event to process.

        Returns:
            None.
        """
        if event.type != pygame.KEYDOWN or self.machine is None:
            return
        if state == GameState.MENU:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.move_selection(-1 if event.key == pygame.K_UP else 1)
            elif event.key == pygame.K_RETURN:
                action = self.select()
                if action == 'START GAME':
                    self.name_error = ''
                    self.machine.game.start_game()
                elif action == 'HIGHSCORES':
                    self.scores = self.high.get_top_scores()
                    self.machine.change_state(GameState.HIGHSCORES)
                elif action == 'INSTRUCTIONS':
                    self.machine.change_state(GameState.INSTRUCTIONS)
                else:
                    self.machine.running = False
        elif state in (GameState.HIGHSCORES, GameState.INSTRUCTIONS):
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.machine.change_state(GameState.MENU)
        elif state == GameState.VICTORY:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.begin_name_input()
        elif state == GameState.NAME_INPUT:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
                self.name_error = ''
            elif event.key == pygame.K_RETURN:
                if not self.high.valid_name(self.player_name):
                    self.name_error = 'Enter 1-10 letters, numbers or spaces.'
                elif self.high.add_score(
                    self.player_name, self.machine.game.game.score
                ):
                    self.scores = self.high.get_top_scores()
                    self.name_error = ''
                    self.machine.change_state(GameState.MENU)
                else:
                    self.name_error = (
                        'Cannot save score. Check the file and retry.'
                    )
            elif (event.unicode and event.unicode.isascii()
                  and (event.unicode.isalnum() or event.unicode == ' ')
                  and len(self.player_name) < 10):
                self.player_name += event.unicode
                self.name_error = ''

    def begin_name_input(self) -> None:
        """Reset entry when a new game finishes.

        Returns:
            None.
        """
        self.player_name = ''
        self.name_error = ''
        if self.machine is not None:
            self.machine.change_state(GameState.NAME_INPUT)

    def run(self, state: GameState, keys: list[pygame.event.Event]) -> None:
        """Process frame input and render the current screen.

        Args:
            state: Screen state whose input or content is being processed.
            keys: Keyboard events collected for the current frame.

        Returns:
            None.
        """
        for event in keys:
            self.handle_keys(state, event)
            if self.machine is not None and self.machine.state != state:
                return
        if state == GameState.MENU:
            self.draw_menu()
        elif state == GameState.HIGHSCORES:
            self.draw_highscore(self.scores)
        elif state == GameState.INSTRUCTIONS:
            self.page(state, 'HOW TO PLAY', 'ENTER / ESC BACK')
            for index, text in enumerate(INSTRUCTIONS):
                self.line(text, .29 + index * .066)
        elif self.machine is not None:
            points = self.machine.game.game.score
            if state == GameState.VICTORY:
                self.page(state, 'YOU WIN!', 'ENTER SAVE YOUR SCORE')
                self.line('Congratulations! Every level cleared.', .36)
                self.line(f'FINAL SCORE: {points}', .5, GOLD, True)
            elif state == GameState.NAME_INPUT:
                self.page(
                    state, 'SAVE YOUR SCORE', 'TYPE YOUR NAME / ENTER SAVE'
                )
                self.line(f'FINAL SCORE: {points}', .32, GOLD)
                self.line(self.player_name + '_', .46, GOLD, True)
                self.line(
                    f'Letters, numbers and spaces: {len(self.player_name)}/10',
                    .59, MUTED,
                )
                self.line(self.name_error or 'Backspace to edit.', .7,
                          ERROR if self.name_error else MUTED)
