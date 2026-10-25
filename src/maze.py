"""Adapt the assigned maze generator without modifying its package."""

from collections import deque
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ui.draw import Draw

from mazegenerator import MazeGenerator

from .parsing import GameConfig

DIRECTIONS = {
    1: (0, -1),  # north
    2: (1, 0),  # east
    4: (0, 1),  # south
    8: (-1, 0),  # west
}


class Maze:
    """Adapt the assigned generator and place its grid inside the window."""

    def __init__(
        self,
        config: GameConfig,
        draw: "Draw",
        level: int = 0,
        window: tuple[int, int] | None = None,
    ) -> None:
        """Generate the level and compute shared tile coordinates.

        Args:
            config: Validated gameplay configuration.
            draw: Drawing helper for the target surface.
            level: Zero-based index of the level to generate.
            window: Window dimensions in pixels, or None to use the drawing
                surface.

        Returns:
            None.

        Raises:
            ValueError: The assigned generator fails to create the maze.
        """
        self.columns = config.levels[level].width
        self.rows = config.levels[level].height
        if window is None:
            if hasattr(draw, "screen") and draw.screen is not None:
                window = (draw.screen.get_width(), draw.screen.get_height())
            else:
                window = (2100, 1800)

        margin = min(window) // 30
        panel_x = margin
        panel_y = window[1] // 6
        panel_width = window[0] - 2 * margin
        panel_height = window[1] - panel_y - 2 * margin
        self.CELL_SIZE = max(
            1, min(panel_width // self.columns, panel_height // self.rows)
        )
        self.WI = self.columns * self.CELL_SIZE
        self.HE = self.rows * self.CELL_SIZE
        self.offset_x = panel_x + (panel_width - self.WI) // 2
        self.offset_y = panel_y + (panel_height - self.HE) // 2

        seed = config.levels[level].seed
        if seed is None:
            seed = 42 if level == 0 else random.randrange(1, 2**31)
        try:
            self.maze_init = MazeGenerator(
                (self.columns, self.rows), perfect=False, seed=seed
            )
        except Exception as error:
            raise ValueError(f"Maze generator failed: {error}") from error
        self.level = level
        self.maze = self.maze_init.maze

        self.draw = draw

    def is_inside(self, x: int, y: int) -> bool:
        """Return whether a cell lies inside the maze.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.

        Returns:
            bool: True when the cell lies inside the maze bounds.
        """
        return 0 <= x < self.columns and 0 <= y < self.rows

    def can_move(self, x: int, y: int, direction: int) -> bool:
        """Check bounds and walls before entering an adjacent cell.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8 left.

        Returns:
            bool: True when the adjacent destination is inside and its wall is
                open.
        """
        if not self.is_inside(x, y):
            return False
        dx, dy = DIRECTIONS[direction]
        return self.is_inside(x + dx, y + dy) and not (
            self.maze[y][x] & direction
        )

    def get_available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        """Perform the get available moves operation.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.

        Returns:
            list[tuple[int, int]]: Adjacent cells reachable through open
                passages.
        """
        paths = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x = x + dx
            new_y = y + dy
            if self.can_move(x, y, direction) and self.is_inside(new_x, new_y):
                paths.append((new_x, new_y))

        return paths

    def grid_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        """Convert a tile to its center in canvas coordinates.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.

        Returns:
            tuple[int, int]: Pixel coordinates of the specified tile center.
        """
        return (
            self.offset_x + x * self.CELL_SIZE + self.CELL_SIZE // 2,
            self.offset_y + y * self.CELL_SIZE + self.CELL_SIZE // 2,
        )

    def pixel_to_grid(self, x: int, y: int) -> tuple[int, int]:
        """Convert canvas coordinates to a maze tile.

        Args:
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.

        Returns:
            tuple[int, int]: Maze column and row containing the pixel position.
        """
        return (
            (x - self.offset_x) // self.CELL_SIZE,
            (y - self.offset_y) // self.CELL_SIZE,
        )

    def get_walkable_positions(self) -> list[tuple[int, int]]:
        """Return centers of cells with at least one passage.

        Returns:
            list[tuple[int, int]]: Pixel centers of all cells with an open
                passage.
        """
        postions = []
        for row_idx, row in enumerate(self.maze):
            for col_idx, value in enumerate(row):
                if value == 15:
                    continue
                center_x, center_y = self.grid_to_pixel(col_idx, row_idx)
                postions.append((center_x, center_y))

        return postions

    def get_the_midlle_possitions(self) -> tuple[int, int]:
        """Find a reachable spawn near the maze center.

        Returns:
            tuple[int, int]: A usable maze column and row near the center.

        Raises:
            ValueError: No usable spawn cell exists.
        """
        centre = (self.columns // 2, self.rows // 2)
        visited = set()
        visited.add(centre)
        heap = deque([centre])
        while heap:
            x, y = heap.popleft()
            if len(self.get_available_moves(x, y)) >= 1:
                return x, y

            for dx, dy in DIRECTIONS.values():
                nx, ny = x + dx, y + dy
                new = nx, ny
                if new in visited or not self.is_inside(*new):
                    continue
                visited.add(new)
                heap.append(new)

        raise ValueError("No valid spawn position")
