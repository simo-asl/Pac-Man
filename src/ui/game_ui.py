"""Render a cached image maze, live HUD and game-state panels."""

import pygame

from ..game import Game, Player
from ..maze import Maze
from .draw import Draw

GOLD = (255, 220, 50)
TEXT = (240, 240, 240)


class GameUi:
    """Keep gameplay values visible around the playable grid."""

    def __init__(
        self, draw: Draw, player: Player, game: Game, maze: Maze
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            draw: Drawing helper used to prepare or display game images.
            player: Player whose lives, position or power state is used.
            game: Current game controller or gameplay state.
            maze: Current maze with walls and grid-to-pixel conversion
                helpers.

        Returns:
            None.
        """
        self.draw, self.player, self.game, self.maze = draw, player, game, maze
        self.width, self.height = draw.screen.get_size()
        self.size = max(18, self.height // 30)
        self.image = pygame.Surface((self.width, self.height))
        painter = Draw(self.image)
        painter.clear((5, 9, 18))
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                painter.draw_maze(
                    x, y, cell, maze.CELL_SIZE, maze.offset_x, maze.offset_y,
                )

    def menu_game(self) -> None:
        """Draw the cached maze, score, lives, level and remaining time.

        Returns:
            None.
        """
        self.draw.draw_image(self.image, 0, 0)
        remaining = max(0, int(self.game.level_time_remaining()))
        values = (
            f'LIVES: {self.player.lives}',
            f'LEVEL: {self.maze.level + 1}/{len(self.game.config.levels)}',
            f'SCORE: {self.game.score}',
            f'TIME: {remaining // 60}:{remaining % 60:02}',
        )
        for index, text in enumerate(values):
            self.draw.draw_text(
                text, self.width * (2 * index + 1) // 8,
                self.height // 30, self.size, GOLD, True,
                max_width=self.width // 5,
            )
        self.draw.draw_text(
            'ARROW KEYS MOVE   P / ESC PAUSE', self.width // 2,
            self.height * 24 // 25, self.size * 3 // 4, TEXT, True,
        )

    def panel(self, title: str, lines: tuple[str, ...]) -> None:
        """Show readable result or pause actions above the frozen maze.

        Args:
            title: Heading shown at the top of the screen or panel.
            lines: Ordered text rows displayed below the panel heading.

        Returns:
            None.
        """
        x, y = self.width // 5, self.height // 4
        width, height = self.width * 3 // 5, self.height // 2
        self.draw.fill_rect(x, y, width, height, (8, 12, 22))
        self.draw.draw_rect(x, y, width, height, GOLD, 2)
        self.draw.draw_text(
            title, self.width // 2, y + height // 8,
            self.size * 2, GOLD, True, max_width=width * 9 // 10,
        )
        for index, text in enumerate(lines):
            self.draw.draw_text(
                text, self.width // 2,
                y + height * (4 + index * 2) // 11,
                self.size, TEXT, True, max_width=width * 9 // 10,
            )
