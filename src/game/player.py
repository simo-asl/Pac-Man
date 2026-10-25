"""Control player movement, lives and temporary power."""

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from ..maze import Maze
    from ..ui.draw import Draw


class Player:
    """Track player movement, lives, power and invincibility.
    """
    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        speed: int = 7,
        lives: int = 3,
    ) -> None:

        """Initialize this object and its runtime dependencies.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            radius: Radius in pixels used for drawing or collision checks.
            speed: Distance moved in pixels on each gameplay update.
            lives: Initial positive number of player lives.

        Returns:
            None.
        """
        self.x: int = x
        self.y: int = y
        self.lives: int = lives
        self.radius: int = radius
        self.speed: int = speed
        self.alive: bool = True
        self.powered_up: bool = False
        self.power_start_time: int = 0
        self.power_duration: int = 10000
        self.target_x: int = x
        self.target_y: int = y
        self.invincible: bool = False
        self.respawn = (x, y)
        self.direction: int = 2
        self.images: dict[int, pygame.Surface] = {}

    def dead(self) -> None:
        """Mark the player as dead to trigger the game-over flow.

        Returns:
            None.
        """
        self.alive = False

    def lose_life(self) -> None:

        """Remove a life and end the game when no lives remain.

        Returns:
            None.
        """
        if self.lives > 0:
            self.lives -= 1
        if self.lives <= 0:
            self.dead()

    def add_life(self) -> None:
        """Grant the player one extra life.

        Returns:
            None.
        """
        self.lives += 1

    def activate_power(self) -> None:
        """Start or refresh the timed power-pellet effect.

        Returns:
            None.
        """
        self.powered_up = True
        self.power_start_time = pygame.time.get_ticks()

    def toggle_invincibility(self) -> None:
        """Toggle protection from lethal ghost collisions.

        Returns:
            None.
        """
        self.invincible = not self.invincible

    def update_power(self) -> None:
        """Expire player power when its configured duration elapses.

        Returns:
            None.
        """
        if self.powered_up:
            if (pygame.time.get_ticks() - self.power_start_time
                    >= self.power_duration):
                self.powered_up = False

    def move(self, maze: "Maze") -> None:
        """Advance this actor toward its next allowed maze cell.

        Args:
            maze: Current maze with walls and grid-to-pixel conversion
                helpers.

        Returns:
            None.
        """
        keys = pygame.key.get_pressed()

        if self.x == self.target_x and self.y == self.target_y:
            cell_x, cell_y = maze.pixel_to_grid(self.x, self.y)

            if keys[pygame.K_LEFT] and maze.can_move(cell_x, cell_y, 8):
                self.target_x -= maze.CELL_SIZE
                self.direction = 8

            elif keys[pygame.K_RIGHT] and maze.can_move(cell_x, cell_y, 2):
                self.target_x += maze.CELL_SIZE
                self.direction = 2

            elif keys[pygame.K_UP] and maze.can_move(cell_x, cell_y, 1):
                self.target_y -= maze.CELL_SIZE
                self.direction = 1

            elif keys[pygame.K_DOWN] and maze.can_move(cell_x, cell_y, 4):
                self.target_y += maze.CELL_SIZE
                self.direction = 4

        if self.x < self.target_x:
            self.x += min(self.speed, self.target_x - self.x)
        elif self.x > self.target_x:
            self.x -= min(self.speed, self.x - self.target_x)
        elif self.y < self.target_y:
            self.y += min(self.speed, self.target_y - self.y)
        elif self.y > self.target_y:
            self.y -= min(self.speed, self.y - self.target_y)

    def draw(self, draw: "Draw") -> None:
        """Draw this actor or its uneaten pellet through the drawing helper.

        Args:
            draw: Drawing helper used to prepare or display game images.

        Returns:
            None.
        """
        if not self.images:
            self.images = {
                direction: draw.load_image(
                    f"assets/player/pacman_{name}_open.png",
                    (self.radius * 2, self.radius * 2),
                )
                for direction, name in (
                    (1, "up"), (2, "right"), (4, "down"), (8, "left"),
                )
            }
        image = self.images[self.direction]
        draw.draw_image(
            image, self.x - image.get_width() // 2,
            self.y - image.get_height() // 2,
        )
