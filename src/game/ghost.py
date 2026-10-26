"""Track ghost sprites and movement between maze cells."""

import time

from ..maze import Maze
from ..ui import Draw

DIRECTION_NAMES = {
    1: "up",
    2: "right",
    4: "down",
    8: "left",
}


class Ghost:
    """Track one ghost, its sprite, movement target and respawn state.
    """
    def __init__(
        self,
        x: int,
        y: int,
        maze: Maze,
        draw: Draw,
        direction: int,
        corner: tuple[int, int],
        kind: str,
        speed: int = 2,
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            x: Maze column.
            y: Maze row.
            maze: Current maze with walls and grid-to-pixel conversion
                helpers.
            draw: Drawing helper used to prepare or display game images.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8
                left.
            corner: Grid coordinates of the ghost home corner.
            kind: Ghost sprite name.
            speed: Distance moved in pixels on each gameplay update.

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
        self.draw = draw
        self.radius = max(2, maze.CELL_SIZE * 2 // 5)
        sprite_size = (self.radius * 2, self.radius * 2)
        self.images = {
            direction: self.draw.load_image(
                f"assets/ghosts/{self.kind}_{name}.png",
                sprite_size,
            )
            for direction, name in DIRECTION_NAMES.items()
        }
        self.maze = maze
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(x, y)
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.frightened_image = self.draw.load_image(
            "assets/ghosts/frightened_blue.png", sprite_size,
        )
        self.eyes_images = {
            direction: self.draw.load_image(
                f"assets/ghosts/eyes_{name}.png", sprite_size,
            )
            for direction, name in DIRECTION_NAMES.items()
        }
        self.time_eaten: float = 0.0

    def get_eaten(self) -> None:
        """Mark the pellet or ghost as eaten.

        Returns:
            None.
        """
        self.mode = "eaten"
        self.time_eaten = time.monotonic()

    def respawn(self) -> None:
        """Restore this ghost to its original corner in chase mode.

        Returns:
            None.
        """
        self.mode = "chase"
        self.x, self.y = self.spawn
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(*self.spawn)
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def move(self, x: int, y: int) -> None:
        """Advance this actor toward its next allowed maze cell.

        Args:
            x: Maze column.
            y: Maze row.

        Returns:
            None.
        """
        self.x = x
        self.y = y
        self.target_x, self.target_y = self.maze.grid_to_pixel(x, y)

    def draw_ghost(self) -> None:
        """Draw the sprite matching the ghost mode and direction.

        Returns:
            None.
        """
        if self.mode == "frightened":
            image = self.frightened_image
        elif self.mode == "eaten":
            image = self.eyes_images[self.direction]
        else:
            image = self.images[self.direction]
        x = self.pixel_x - image.get_width() // 2
        y = self.pixel_y - image.get_height() // 2
        self.draw.draw_image(image, x, y)

    def update(self) -> None:
        """Advance the ghost pixel position toward its current target.

        Returns:
            None.
        """
        if self.pixel_x < self.target_x:
            self.pixel_x = min(self.speed + self.pixel_x, self.target_x)
        elif self.pixel_x > self.target_x:
            self.pixel_x = max(self.pixel_x - self.speed, self.target_x)

        if self.pixel_y < self.target_y:
            self.pixel_y = min(self.pixel_y + self.speed, self.target_y)
        elif self.pixel_y > self.target_y:
            self.pixel_y = max(self.pixel_y - self.speed, self.target_y)

    def is_at_target(self) -> bool:
        """Check whether the ghost has reached its next cell center.

        Returns:
            True when the ghost is exactly at its target pixel position.
        """
        return self.pixel_x == self.target_x and self.pixel_y == self.target_y
