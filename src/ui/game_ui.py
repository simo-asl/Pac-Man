"""Render a cached image maze, live HUD and game-state panels."""

import pygame

from ..game import Game, Player
from ..maze import Maze
from .draw import FONT_GLYPH_HEIGHT, Draw
from .theme import GOLD, PANEL_BACKGROUND, TEXT


class GameUi:
    """Keep gameplay values visible around the playable grid."""

    def __init__(
        self, drawer: Draw, player: Player, game: Game, maze: Maze
    ) -> None:
        """Bind gameplay values and cache the static maze background.

        Args:
            drawer: Drawing helper used to prepare or display game images.
            player: Player whose lives, position or power state is used.
            game: Current game controller or gameplay state.
            maze: Current maze with walls and grid-to-pixel conversion
                helpers.

        Returns:
            None.
        """
        self.drawer = drawer
        self.player = player
        self.game = game
        self.maze = maze
        self.window_width, self.window_height = drawer.screen.get_size()
        self.font_scale = max(1, self.window_height // 600)
        self.maze_image = self._build_maze_image()

    def _build_maze_image(self) -> pygame.Surface:
        """Prepare a static wall image for the current level.

        Returns:
            Cached background and maze walls at the window resolution.
        """
        maze_image = pygame.Surface((self.window_width, self.window_height))
        maze_drawer = Draw(maze_image)
        maze_drawer.clear((5, 9, 18))
        for row_index, maze_row in enumerate(self.maze.maze):
            for column_index, wall_mask in enumerate(maze_row):
                maze_drawer.draw_maze(
                    column_index, row_index, wall_mask, self.maze.CELL_SIZE,
                    self.maze.offset_x, self.maze.offset_y,
                )
        return maze_image

    def draw_game(self) -> None:
        """Draw the cached maze, score, lives, level and remaining time.

        Returns:
            None.
        """
        self.drawer.draw_image(self.maze_image, 0, 0)
        self._draw_hud()

    def _draw_hud(self) -> None:
        """Display live game values and the gameplay control hint.

        Returns:
            None.
        """
        if self.game.arcade_survival:
            survived = self.game.survival_time()
            hud_labels = (
                f'LIVES: {self.player.lives}',
                f'SCORE: {self.game.score}',
                f'TIME: {survived // 60:02}:{survived % 60:02}',
                f'WAVE: {self.game.wave}',
            )
        else:
            remaining_seconds = max(0, int(self.game.level_time_remaining()))
            hud_labels = (
                f'LIVES: {self.player.lives}',
                f'LEVEL: {self.maze.level + 1}/{len(self.game.config.levels)}',
                f'SCORE: {self.game.score}',
                f'TIME: {remaining_seconds // 60}:{remaining_seconds % 60:02}',
            )
        for index, text in enumerate(hud_labels):
            self.drawer.draw_text(
                text, self.window_width * (2 * index + 1) // 8,
                self.window_height // 30, self.font_scale, GOLD, True,
                max_width=self.window_width // 5,
            )
        self.drawer.draw_text(
            'ARROW KEYS MOVE   P / ESC PAUSE', self.window_width // 2,
            self.window_height * 24 // 25, 1, TEXT, True,
        )

    def draw_panel(self, title: str, lines: tuple[str, ...]) -> None:
        """Show readable result or pause actions above the frozen maze.

        Args:
            title: Heading shown at the top of the screen or panel.
            lines: Ordered text rows displayed below the panel heading.

        Returns:
            None.
        """
        panel_x = self.window_width // 5
        panel_y = self.window_height // 4
        panel_width = self.window_width * 3 // 5
        panel_height = self.window_height // 2
        self.drawer.fill_rect(
            panel_x, panel_y, panel_width, panel_height, PANEL_BACKGROUND,
        )
        self.drawer.draw_rect(
            panel_x, panel_y, panel_width, panel_height, GOLD, 2,
        )
        self.drawer.draw_text(
            title, self.window_width // 2, panel_y + panel_height // 8,
            self.font_scale * 2, GOLD, True, max_width=panel_width * 9 // 10,
        )
        row_height = panel_height * 3 // 5 // max(1, len(lines))
        text_scale = self.font_scale
        while text_scale > 1 and text_scale * FONT_GLYPH_HEIGHT > row_height:
            text_scale -= 1
        for index, text in enumerate(lines):
            self.drawer.draw_text(
                text, self.window_width // 2,
                panel_y + panel_height // 3 + index * row_height,
                text_scale, TEXT, True, max_width=panel_width * 9 // 10,
            )
