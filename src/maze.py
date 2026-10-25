"""Adapt the assigned maze generator without changing its package."""

import random
from typing import TYPE_CHECKING

from mazegenerator import MazeGenerator

if TYPE_CHECKING:
    from .ui.draw import Draw

from .parsing import GameConfig

color38 = (255, 153, 204)
color39 = (204, 153, 255)
color40 = (255, 204, 153)

DIRECTIONS = {
    1: (0, -1),  # north
    2: (1, 0),  # east
    4: (0, 1),  # south
    8: (-1, 0),  # west
}


class Maze:
    """Adapt the assigned generator and map grid cells to window pixels.
    """
    def __init__(
        self,
        config: GameConfig,
        draw: "Draw",
        level: int = 0,
        window: tuple[int, int] | None = None,
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            config: Validated game configuration.
            draw: Drawing helper used to prepare or display game images.
            level: Zero-based index of the configured level.
            window: Window width and height in pixels; None uses the draw
                target.

        Returns:
            None.
        """

        self.columns = config.levels[level].width
        self.rows = config.levels[level].height
        if window is None:
            if hasattr(draw, "screen") and draw.screen is not None:
                window = (draw.screen.get_width(), draw.screen.get_height())
            else:
                window = (1800, 1200)

        self.CELL_SIZE = max(1, int(
            min(window[0] // self.columns, window[1] // self.rows) * 0.80
        ))

        self.WI = self.columns * self.CELL_SIZE
        self.HE = self.rows * self.CELL_SIZE
        self.offset_x = (window[0] - self.WI) // 2
        self.offset_y = (window[1] - self.HE) // 2

        seed = config.levels[level].seed
        if seed is None:
            seed = 42 if level == 0 else random.randrange(1, 2**31)
        self.maze_init = MazeGenerator(
            (self.columns, self.rows), perfect=False, seed=seed,
        )

        self.level = level
        self.maze = self.maze_init.maze

        self.draw = draw

    def is_inside(self, x: int, y: int) -> bool:
        """Check whether grid coordinates lie within the maze.

        Args:
            x: Maze column.
            y: Maze row.

        Returns:
            True if the cell is inside the maze bounds.
        """
        return 0 <= x < self.columns and 0 <= y < self.rows

    def can_move(self, x: int, y: int, direction: int) -> bool:
        """Check the current cell wall before entering an adjacent cell.

        Args:
            x: Maze column.
            y: Maze row.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8
                left.

        Returns:
            True if the current cell has no wall in that direction.
        """
        if not self.is_inside(x, y):
            return False
        return not (self.maze[y][x] & direction)

    def get_available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        """Find adjacent cells reachable through open walls.

        Args:
            x: Maze column.
            y: Maze row.

        Returns:
            Reachable neighboring grid coordinates.
        """
        paths = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x = x + dx
            new_y = y + dy
            if self.can_move(x, y, direction) and self.is_inside(new_x, new_y):
                paths.append((new_x, new_y))

        return paths

    def grid_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        """Convert a maze cell to the pixel position of its center.

        Args:
            x: Maze column.
            y: Maze row.

        Returns:
            Horizontal and vertical pixel coordinates of the cell center.
        """
        return (
            self.offset_x + x * self.CELL_SIZE + self.CELL_SIZE // 2,
            self.offset_y + y * self.CELL_SIZE + self.CELL_SIZE // 2,
        )

    def pixel_to_grid(self, x: int, y: int) -> tuple[int, int]:
        """Convert a window pixel position to maze cell coordinates.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.

        Returns:
            Column and row containing the pixel position.
        """
        return (
            (x - self.offset_x) // self.CELL_SIZE,
            (y - self.offset_y) // self.CELL_SIZE,
        )

    def get_walkable_positions(self) -> list[tuple[int, int]]:
        """Collect the pixel centers of nonblocked cells.

        Returns:
            Pixel centers of all cells with at least one opening.
        """
        postions = []
        for row_idx, row in enumerate(self.maze):
            for col_idx, value in enumerate(row):
                if value == 15:
                    continue
                center_x, center_y = self.grid_to_pixel(col_idx, row_idx)
                postions.append((center_x, center_y))

        return postions
