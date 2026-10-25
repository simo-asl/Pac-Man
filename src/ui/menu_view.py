"""Render menu pages without handling navigation or persistent scores."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .content import INSTRUCTIONS
from .draw import Color, Draw
from .state import GameState
from .theme import ERROR, GOLD, MUTED, PANEL_BACKGROUND, TEXT

if TYPE_CHECKING:
    import pygame
    from ..game.highscore import score


class MenuView:
    """Own menu artwork, text placement, and page-specific layouts."""

    def __init__(self, drawer: Draw) -> None:
        """Load the artwork and establish menu typography.

        Args:
            drawer: Drawing target used for every menu page.

        Returns:
            None.
        """
        self.drawer = drawer
        self.window_width, self.window_height = drawer.screen.get_size()
        self.font_size = max(18, self.window_height // 32)
        self.background_images: dict[GameState, pygame.Surface] = {}
        background_files = (
            (GameState.MENU, 'main_menu.png'),
            (GameState.HIGHSCORES, 'highscores.png'),
            (GameState.INSTRUCTIONS, 'instructions.png'),
            (GameState.VICTORY, 'victory_image.png'),
            (GameState.NAME_INPUT, 'name_input.png'),
        )
        window_size = (self.window_width, self.window_height)
        for state, filename in background_files:
            image_path = f'assets/backgrounds/{filename}'
            background = drawer.load_image(image_path, window_size)
            self.background_images[state] = background

    def _draw_line(
        self, text: str, vertical_fraction: float, color: Color = TEXT,
        is_heading: bool = False,
    ) -> None:
        """Place centered text inside the artwork's clear middle area.

        Args:
            text: Text to measure or render.
            vertical_fraction: Vertical position as a fraction of the
                window height.
            color: RGB color for the pixels, outline or text.
            is_heading: Whether to use the larger heading font size.

        Returns:
            None.
        """
        center_x = self.window_width // 2
        text_y = int(self.window_height * vertical_fraction)
        font_size = self.font_size
        if is_heading:
            font_size *= 2
        maximum_width = self.window_width * 3 // 5
        self.drawer.draw_text(
            text, center_x, text_y, font_size,
            color, True, max_width=maximum_width,
        )

    def _draw_page(self, state: GameState, title: str, hint: str) -> None:
        """Frame content with the original artwork and a readable panel.

        Args:
            state: Screen state whose input or content is being processed.
            title: Heading shown at the top of the screen or panel.
            hint: Keyboard guidance shown at the bottom of the page.

        Returns:
            None.
        """
        self.drawer.draw_image(self.background_images[state], 0, 0)
        self.drawer.fill_rect(
            self.window_width // 5, self.window_height // 10,
            self.window_width * 3 // 5, self.window_height * 4 // 5,
            PANEL_BACKGROUND,
        )
        self.drawer.draw_rect(
            self.window_width // 5, self.window_height // 10,
            self.window_width * 3 // 5, self.window_height * 4 // 5, GOLD, 2,
        )
        self._draw_line(title, .15, GOLD, True)
        self._draw_line(hint, .83, MUTED)

    def draw_menu(
        self, options: list[str], selected_index: int, error_message: str
    ) -> None:
        """Show all four required main-menu actions.

        Args:
            options: Labels of the available main-menu actions.
            selected_index: Index of the action highlighted by the keyboard.
            error_message: Startup feedback; empty when no error is present.

        Returns:
            None.
        """
        self._draw_page(
            GameState.MENU, 'PAC-MAN', 'UP / DOWN SELECT   ENTER CONFIRM'
        )
        for index, option in enumerate(options):
            self._draw_line(
                ('> ' if index == selected_index else '') + option,
                .34 + index * .1,
                GOLD if index == selected_index else TEXT,
            )
        if error_message:
            self._draw_line(error_message, .76, ERROR)

    def draw_highscore(self, scores: list[score]) -> None:
        """Fit all ten entries, with separate columns for names and scores.

        Args:
            scores: Ranked highscore entries to display, limited to ten.

        Returns:
            None.
        """
        self._draw_page(
            GameState.HIGHSCORES, 'HIGH SCORES', 'ENTER / ESC BACK',
        )
        if not scores:
            self._draw_line('No scores yet. Start your first game!', .46)
        for index, entry in enumerate(scores[:10]):
            score_row_y = int(self.window_height * (.28 + index * .048))
            self.drawer.draw_text(
                f'{index + 1:2}.  {entry.name}', self.window_width * 6 // 25,
                score_row_y, self.font_size, GOLD if index == 0 else TEXT,
                max_width=self.window_width * 3 // 10,
            )
            self.drawer.draw_text(
                str(entry.score), self.window_width * 17 // 25, score_row_y,
                self.font_size, TEXT, True, max_width=self.window_width // 7,
            )

    def draw_instructions(self) -> None:
        """Display shared controls and rules.

        Returns:
            None.
        """
        self._draw_page(
            GameState.INSTRUCTIONS, 'HOW TO PLAY', 'ENTER / ESC BACK',
        )
        for index, instruction in enumerate(INSTRUCTIONS):
            self._draw_line(instruction, .29 + index * .066)

    def draw_victory(self, final_score: int) -> None:
        """Show the win message and final score.

        Args:
            final_score: Score earned by the completed game.

        Returns:
            None.
        """
        self._draw_page(GameState.VICTORY, 'YOU WIN!', 'ENTER SAVE YOUR SCORE')
        self._draw_line('Congratulations! Every level cleared.', .36)
        self._draw_line(f'FINAL SCORE: {final_score}', .5, GOLD, True)

    def draw_name_input(
        self, final_score: int, player_name: str, error_message: str
    ) -> None:
        """Show name-entry text and validation feedback.

        Args:
            final_score: Score awaiting persistence.
            player_name: Current contents of the name field.
            error_message: Validation or save error, or an empty string.

        Returns:
            None.
        """
        self._draw_page(
            GameState.NAME_INPUT, 'SAVE YOUR SCORE',
            'TYPE YOUR NAME / ENTER SAVE',
        )
        self._draw_line(f'FINAL SCORE: {final_score}', .32, GOLD)
        self._draw_line(player_name + '_', .46, GOLD, True)
        self._draw_line(
            f'Letters, numbers and spaces: {len(player_name)}/10', .59, MUTED,
        )
        self._draw_line(error_message or 'Backspace to edit.', .7,
                        ERROR if error_message else MUTED)
