"""Represent a ghost with smooth tile-based movement."""

import time

import pygame

from ..maze import Maze
from ..ui import Draw


class Ghost:
    """Represent a ghost and its movement state."""

    BASE_SPEED = 2.5  # Tiles per second.

    def __init__(
        self,
        x: int,
        y: int,
        maze: Maze,
        draw: Draw,
        direction: int,
        corner: tuple[int, int],
        kind: str,
        speed: float = BASE_SPEED,
    ) -> None:
        """Initialize this object and its dependencies.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.
            maze: Current maze and its coordinate conversion helpers.
            draw: Drawing helper for the target surface.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8 left.
            corner: Home corner as a pair of maze column and row indices.
            kind: Ghost name used to select its appearance and chase behavior.
            speed: Movement speed in tiles per second.

        Returns:
            None.
        """
        self.x = x
        self.y = y
        self.spawn = (x, y)
        self.direction = direction
        self.corner = corner
        self.kind = kind
        self.mode = "chase"
        self.speed = speed
        self.movement_remainder = 0.0
        self.draw = draw
        self.radius = max(3, maze.CELL_SIZE * 2 // 5)
        self.image = pygame.transform.smoothscale(
            self.draw.load_image(f"src/assets/arcade/{self.kind}.png"),
            (self.radius * 2, self.radius * 2),
        )
        self.maze = maze
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(x, y)
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.frightened_image = pygame.transform.smoothscale(
            self.draw.load_image("src/assets/arcade/frightened.png"),
            self.image.get_size(),
        )
        self.time_eaten: float = 0.0

    def get_eaten(self) -> None:
        """Mark this item or ghost as eaten.

        Returns:
            None.
        """
        self.mode = "eaten"
        self.time_eaten = time.monotonic()

    def respawn(self) -> None:
        """Return the ghost to its assigned corner in chase mode.

        Returns:
            None.
        """
        self.mode = "chase"
        self.movement_remainder = 0.0
        self.x, self.y = self.spawn
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(*self.spawn)
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def move(self, x: int, y: int) -> None:
        """Move toward the next allowed tile.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.

        Returns:
            None.
        """
        self.x = x
        self.y = y
        self.target_x, self.target_y = self.maze.grid_to_pixel(x, y)

    def draw_ghost(self) -> None:
        """Render the current normal, frightened or eaten appearance.

        Returns:
            None.
        """
        if self.mode == "frightened":
            image = self.frightened_image
        elif self.mode == "eaten":
            self.draw.draw_circle(
                self.pixel_x - self.radius // 3,
                self.pixel_y,
                max(1, self.radius // 4),
                (255, 255, 255),
            )
            self.draw.draw_circle(
                self.pixel_x + self.radius // 3,
                self.pixel_y,
                max(1, self.radius // 4),
                (255, 255, 255),
            )
            return
        else:
            image = self.image
        x = self.pixel_x - image.get_width() // 2
        y = self.pixel_y - image.get_height() // 2
        self.draw.draw_image(image, x, y)

    def update(self, delta_time: float = 1 / 60) -> None:
        """Move at a consistent tile speed without overshooting a turn.

        Args:
            delta_time: Elapsed active-frame time in seconds.

        Returns:
            None.
        """
        distance = max(
            abs(self.target_x - self.pixel_x),
            abs(self.target_y - self.pixel_y),
        )
        if distance == 0:
            self.movement_remainder = 0.0
            return
        factor = 0.6 if self.mode == "frightened" else 1.0
        self.movement_remainder += (
            self.speed
            * self.maze.CELL_SIZE
            * min(max(delta_time, 0), 0.05)
            * factor
        )
        step = min(int(self.movement_remainder), distance)
        self.movement_remainder -= step
        if self.pixel_x != self.target_x:
            self.pixel_x += step if self.target_x > self.pixel_x else -step
        elif self.pixel_y != self.target_y:
            self.pixel_y += step if self.target_y > self.pixel_y else -step

    def is_at_target(self) -> bool:
        """Return whether the ghost has reached its target tile.

        Returns:
            bool: True when the ghost has reached its next tile center.
        """
        return self.pixel_x == self.target_x and self.pixel_y == self.target_y
