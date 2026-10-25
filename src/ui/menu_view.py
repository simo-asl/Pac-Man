"""Draw menu pages; navigation and score saving live in menu.py."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from .background import background
from .draw import Draw
from .panels import ERROR, GOLD, LINE, MUTED, TEXT, choice, panel, result

if TYPE_CHECKING:
    from ..game.highscore import score


class MenuView:
    """Render the existing artwork with consistent, readable page layouts."""

    def __init__(self, draw: Draw) -> None:
        """Prepare the background and original Pac-Man image once.

        Args:
            draw: Drawing helper for the target surface.

        Returns:
            None.
        """
        self.draw = draw
        self.width, self.height = draw.screen.get_size()
        self.size = max(24, min(self.width // 30, self.height // 32))
        self.title_size = self.size * 5 // 2
        self.background = background(draw)
        hero = draw.load_image("src/assets/arcade/player_right.png")
        side = self.height // 20
        self.hero = pygame.transform.smoothscale(hero, (side, side))

    def page(
        self,
        title: str,
        hint: str = "ENTER / ESC  BACK TO MENU",
    ) -> None:
        """Draw an image frame, heading and screen-specific keyboard hint.

        Args:
            title: Heading displayed at the top of the page or result card.
            hint: Keyboard action displayed for the current screen.

        Returns:
            None.
        """
        self.draw.draw_image(self.background, 0, 0)
        self.draw.draw_text(
            title,
            self.width // 2,
            self.height * 13 // 100,
            self.title_size,
            GOLD,
            True,
            max_width=self.width * 3 // 4,
        )
        self.draw.draw_text(
            hint,
            self.width // 2,
            self.height * 9 // 10,
            self.size * 3 // 4,
            MUTED,
            True,
            max_width=self.width * 3 // 4,
        )

    def main(self, options: list[str], selected: int, error: str) -> None:
        """Make Start Game and the current keyboard selection obvious.

        Args:
            options: Labels of the available main-menu actions.
            selected: Zero-based index of the highlighted option.
            error: Validation, save or startup feedback; empty when there is no
                error.

        Returns:
            None.
        """
        self.page("PAC-MAN", "UP / DOWN  SELECT    ENTER  CONFIRM")
        self.draw.draw_text(
            "Clear the maze. Beat your best.",
            self.width // 2,
            self.height // 5,
            self.size * 3 // 4,
            MUTED,
            True,
        )
        self.draw.draw_image(
            self.hero,
            (self.width - self.hero.get_width()) // 2,
            self.height * 6 // 25,
        )
        for index, label in enumerate(options):
            rect = pygame.Rect(
                self.width // 4,
                self.height * 39 // 100 + index * self.height // 12,
                self.width // 2,
                self.height // 15,
            )
            choice(self.draw, rect, label, self.size, index == selected)
        if error:
            self.draw.draw_text(
                error,
                self.width // 2,
                self.height * 4 // 5,
                self.size * 3 // 4,
                ERROR,
                True,
                max_width=self.width * 3 // 4,
            )

    def highscores(self, scores: list[score]) -> None:
        """Align ranks, names and scores in a single top-ten table.

        Args:
            scores: Ranked saved entries to display, limited to the top ten.

        Returns:
            None.
        """
        self.page("HIGH SCORES")
        rect = pygame.Rect(
            self.width // 6,
            self.height // 3,
            self.width * 2 // 3,
            self.height * 23 // 50,
        )
        panel(self.draw, rect)
        row_height = rect.height // 12
        rank_x = rect.x + rect.width // 20
        name_x = rect.x + rect.width // 5
        score_x = rect.right - rect.width // 20
        header_y = rect.y + row_height // 2
        for label, x in (("#", rank_x), ("PLAYER", name_x)):
            self.draw.draw_text(
                label,
                x,
                header_y,
                self.size * 2 // 3,
                MUTED,
            )
        self.draw.draw_text(
            "SCORE",
            score_x - self.draw.measure_text("SCORE", self.size * 2 // 3)[0],
            header_y,
            self.size * 2 // 3,
            MUTED,
        )
        if not scores:
            self.draw.draw_text(
                "No scores yet. Start your first game!",
                rect.centerx,
                rect.centery,
                self.size,
                TEXT,
                True,
                max_width=rect.width * 4 // 5,
            )
        for index, entry in enumerate(scores[:10]):
            y = rect.y + (index + 2) * row_height
            color = GOLD if index == 0 else TEXT
            self.draw.draw_horizontal_line(
                rank_x,
                y - row_height // 5,
                score_x,
                LINE,
            )
            self.draw.draw_text(
                str(index + 1),
                rank_x,
                y,
                self.size,
                MUTED,
            )
            self.draw.draw_text(
                entry.name,
                name_x,
                y,
                self.size,
                color,
                max_width=rect.width * 2 // 5,
            )
            value = str(entry.score)
            size = self.draw.fit_text(value, self.size, rect.width // 3)
            width = self.draw.measure_text(value, size)[0]
            self.draw.draw_text(value, score_x - width, y, size, color)

    def instructions(self) -> None:
        """Explain controls and rules on a static page, with no selection.

        Returns:
            None.
        """
        self.page("HOW TO PLAY")
        rect = pygame.Rect(
            self.width // 6,
            self.height * 3 // 10,
            self.width * 2 // 3,
            self.height // 2,
        )
        panel(self.draw, rect)
        left = rect.x + rect.width // 12
        for index, (label, keys) in enumerate(
            (
                ("MOVE", "ARROW KEYS"),
                ("PAUSE / RESUME", "P / ESC"),
            )
        ):
            y = rect.y + rect.height * (1 + index) // 9
            self.draw.draw_text(label, left, y, self.size, TEXT)
            self.draw.draw_text(
                keys,
                rect.x + rect.width * 3 // 5,
                y,
                self.size,
                GOLD,
            )
        rules = (
            "Eat every pellet to finish the level.",
            "Power pellets let you eat blue ghosts.",
            "Avoid ghosts. Losing all lives ends the game.",
            "Clear every level and watch the timer.",
        )
        for index, text in enumerate(rules):
            self.draw.draw_text(
                text,
                left,
                rect.y + rect.height * (4 + index) // 9,
                self.size * 4 // 5,
                TEXT,
                max_width=rect.width * 5 // 6,
            )
        self.draw.draw_text(
            "CHEATS  I: invincible   F: freeze   L: life   S: skip",
            rect.centerx,
            rect.bottom - rect.height // 9,
            self.size * 2 // 3,
            MUTED,
            True,
            max_width=rect.width * 5 // 6,
        )

    def victory(self, score: int) -> None:
        """Celebrate completion with the same result layout as Game Over.

        Args:
            score: Actual game score to display.

        Returns:
            None.
        """
        self.draw.draw_image(self.background, 0, 0)
        result(
            self.draw,
            "YOU WIN!",
            score,
            "ENTER  SAVE YOUR SCORE",
            message="Every level cleared. Well played!",
        )

    def name_input(self, score: int, name: str, error: str) -> None:
        """Show a focused input field, name limit and validation feedback.

        Args:
            score: Actual game score to display.
            name: Player name to validate, display or save.
            error: Validation, save or startup feedback; empty when there is no
                error.

        Returns:
            None.
        """
        self.page("SAVE YOUR SCORE", "TYPE YOUR NAME    ENTER  SAVE")
        rect = pygame.Rect(
            self.width // 6,
            self.height // 3,
            self.width * 2 // 3,
            self.height * 2 // 5,
        )
        panel(self.draw, rect)
        self.draw.draw_text(
            f"FINAL SCORE   {score}",
            rect.centerx,
            rect.y + rect.height // 8,
            self.size,
            GOLD,
            True,
            max_width=rect.width * 4 // 5,
        )
        field = pygame.Rect(
            rect.x + rect.width // 10,
            rect.y + rect.height * 3 // 8,
            rect.width * 4 // 5,
            rect.height // 5,
        )
        panel(self.draw, field, GOLD)
        value = name + "_" if name else "Type your name"
        text_height = self.draw.measure_text(value, self.size)[1]
        self.draw.draw_text(
            value,
            field.centerx,
            field.centery - text_height // 2,
            self.size,
            GOLD if name else MUTED,
            True,
            max_width=field.width * 9 // 10,
        )
        self.draw.draw_text(
            f"Letters, numbers and spaces   {len(name)}/10",
            rect.centerx,
            rect.y + rect.height * 5 // 8,
            self.size * 2 // 3,
            MUTED,
            True,
            max_width=rect.width * 4 // 5,
        )
        self.draw.draw_text(
            error or "Backspace to edit. A name is required.",
            rect.centerx,
            rect.y + rect.height * 4 // 5,
            self.size * 3 // 4,
            ERROR if error else TEXT,
            True,
            max_width=rect.width * 4 // 5,
        )
