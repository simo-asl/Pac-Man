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
        self.x = x
        self.y = y
        self.spawn = (x, y)
        self.direction = direction
        self.corner = corner
        self.kind = kind
        self.mode = "chase"
        self.speed = speed
        self.draw = draw
        self.images = {
            direction: self.draw.load_image(
                f"src/game/assets/ghosts/{self.kind}_{name}.png"
            )
            for direction, name in DIRECTION_NAMES.items()
        }
        self.maze = maze
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(x, y)
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.frightened_image = self.draw.load_image(
            "src/game/assets/ghosts/frightened_blue.png"
        )
        self.eyes_images = {
            direction: self.draw.load_image(f"src/game/assets/ghosts/eyes_{name}.png")
            for direction, name in DIRECTION_NAMES.items()
        }
        self.time_eaten: float = 0.0

    def get_eaten(self) -> None:
        self.mode = "eaten"
        self.time_eaten = time.monotonic()

    def respawn(self) -> None:
        self.mode = "chase"
        self.x, self.y = self.spawn
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(*self.spawn)
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.target_x, self.target_y = self.maze.grid_to_pixel(x, y)

    def draw_ghost(self) -> None:
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
        if self.pixel_x < self.target_x:
            self.pixel_x = min(self.speed + self.pixel_x, self.target_x)
        elif self.pixel_x > self.target_x:
            self.pixel_x = max(self.pixel_x - self.speed, self.target_x)

        if self.pixel_y < self.target_y:
            self.pixel_y = min(self.pixel_y + self.speed, self.target_y)
        elif self.pixel_y > self.target_y:
            self.pixel_y = max(self.pixel_y - self.speed, self.target_y)

    def is_at_target(self) -> bool:
        return self.pixel_x == self.target_x and self.pixel_y == self.target_y
