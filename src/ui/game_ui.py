"""Render the gameplay HUD, cached maze, pause and result screens."""

import pygame

from ..game import Game, Player
from ..game.highscore import High
from ..maze import Maze
from .background import background
from .draw import Draw
from .panels import ERROR, GOLD, LINE, MUTED, TEXT, pause, result


class GameUi:
    """Render gameplay, pause and end overlays."""

    def __init__(
        self, draw: Draw, player: Player, game: Game, maze: Maze
    ) -> None:
        """Initialize this object and its dependencies.

        Args:
            draw: Drawing helper for the target surface.
            player: Player whose position, lives or power state is used.
            game: Active game state, score and timing information.
            maze: Current maze and its coordinate conversion helpers.

        Returns:
            None.
        """
        self.draw = draw
        self.player = player
        self.game = game
        self.maze = maze

        self.width, self.height = self.draw.screen.get_size()
        self.font_size = max(20, self.height // 30)
        scores = High(game.config.highscore_filename).get_top_scores()
        self.best_score = scores[0].score if scores else 0

        self.background = background(draw)

        # Reuse the static maze; only gameplay objects and the HUD change each
        # frame.
        self.maze_surface: pygame.Surface | None = None

        # Reuse one translucent overlay for pause and end screens.
        self.overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.overlay.fill((0, 0, 0, 185))

    def menu_game(self) -> None:
        """Draw the cached maze background and the changing HUD.

        Returns:
            None.
        """
        if self.maze_surface is None:
            surface = self.background.copy()
            # Quiet the artwork behind the always-visible game values.
            margin = self.width // 30
            surface.fill(
                (13, 20, 31),
                (
                    margin,
                    self.height // 40,
                    self.width - 2 * margin,
                    self.height // 9,
                ),
            )

            offset_x = self.maze.offset_x
            offset_y = self.maze.offset_y

            # Keep decorative artwork outside the actual playable grid.
            padding = max(2, self.maze.CELL_SIZE // 5)
            surface.fill(
                (9, 15, 25),
                (
                    offset_x - padding,
                    offset_y - padding,
                    self.maze.WI + 2 * padding,
                    self.maze.HE + 2 * padding,
                ),
            )
            surface_draw = Draw(surface)
            surface_draw.draw_rect(
                offset_x - padding,
                offset_y - padding,
                self.maze.WI + 2 * padding,
                self.maze.HE + 2 * padding,
                LINE,
                2,
            )
            # Supersample only the cached walls for smooth rounded corners.
            walls = pygame.Surface(
                (self.maze.WI * 2, self.maze.HE * 2),
                pygame.SRCALPHA,
            )
            wall_draw = Draw(walls)
            for y, row in enumerate(self.maze.maze):
                for x, cell in enumerate(row):
                    wall_draw.draw_maze(
                        x,
                        y,
                        cell,
                        self.maze.CELL_SIZE * 2,
                    )
            surface.blit(
                pygame.transform.smoothscale(
                    walls,
                    (self.maze.WI, self.maze.HE),
                ),
                (offset_x, offset_y),
            )

            self.maze_surface = surface

        self.draw.screen.blit(self.maze_surface, (0, 0))
        self.draw_hud()

    def draw_hud(self) -> None:
        """Render live game values and the controls hint.

        Returns:
            None.
        """
        time_left = max(0, int(self.game.level_time_remaining()))
        values = (
            ("LIVES", str(self.player.lives)),
            (
                "LEVEL",
                f"{self.maze.level + 1} / {len(self.game.config.levels)}",
            ),
            ("SCORE", str(self.game.score)),
            ("TIME", f"{time_left // 60}:{time_left % 60:02}"),
            ("BEST", str(max(self.best_score, self.game.score))),
        )
        # Center the live values evenly across the HUD.
        for index, (label, value) in enumerate(values):
            x = self.width * (2 * index + 1) // (2 * len(values))
            self.draw.draw_text(
                label,
                x,
                self.height // 25,
                self.font_size * 2 // 3,
                MUTED,
                True,
            )
            self.draw.draw_text(
                value,
                x,
                self.height // 12,
                (
                    self.font_size * 4 // 3
                    if label == "SCORE"
                    else self.font_size
                ),
                ERROR
                if label == "TIME" and time_left <= 10
                else GOLD
                if label == "SCORE"
                else TEXT,
                True,
                max_width=self.width // 6,
            )
        self.draw.draw_horizontal_line(
            self.width // 30,
            self.height // 7,
            self.width * 29 // 30,
            LINE,
        )
        self.draw.draw_text(
            "ARROW KEYS  MOVE     P / ESC  PAUSE",
            self.width // 2,
            self.height * 24 // 25,
            self.font_size * 2 // 3,
            TEXT,
            True,
        )

    def draw_paused(self, selected: int = 0) -> None:
        """Dim the frozen game and show its selected pause action.

        Args:
            selected: Zero-based index of the highlighted option.

        Returns:
            None.
        """
        self.draw.draw_image(self.overlay, 0, 0)
        pause(self.draw, selected)

    def draw_game_over(self) -> None:
        """Show the final score and the next action.

        Returns:
            None.
        """
        self.draw.draw_image(self.overlay, 0, 0)
        result(
            self.draw,
            "GAME OVER",
            self.game.score,
            "ENTER  SAVE YOUR SCORE",
            ERROR,
        )

    def draw_level_complete(self) -> None:
        """Show the current score and let the player continue.

        Returns:
            None.
        """
        self.draw.draw_image(self.overlay, 0, 0)
        result(
            self.draw,
            "LEVEL COMPLETE",
            self.game.score,
            "ENTER  NEXT LEVEL",
            score_label="SCORE",
        )
