"""Control player movement, lives and temporary power."""

from typing import TYPE_CHECKING

import pygame

from ..resources import resource_path

if TYPE_CHECKING:
    from ..maze import Maze


class Player:
    """Control player movement, lives and power."""

    def __init__(
        self,
        x: int,
        y: int,
        radius: int,
        s_width: int = 900,
        s_height: int = 900,
        speed: int = 7,
        lives: int = 3,
    ) -> None:
        """Initialize this object and its dependencies.

        Args:
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.
            radius: Radius in pixels for drawing or collision detection.
            s_width: Width of the game area in pixels.
            s_height: Height of the game area in pixels.
            speed: Movement in pixels per player update.
            lives: Initial number of remaining player lives.

        Returns:
            None.
        """
        self.x: int = x
        self.y: int = y
        self.lives: int = lives
        self.radius: int = radius
        self.s_width: int = s_width
        self.s_height: int = s_height
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
        self.images = {
            direction: pygame.transform.smoothscale(
                pygame.image.load(
                    str(resource_path(f"src/assets/arcade/player_{name}.png"))
                ).convert_alpha(),
                (radius * 2, radius * 2),
            )
            for direction, name in (
                (1, "up"),
                (2, "right"),
                (4, "down"),
                (8, "left"),
            )
        }

    def dead(self) -> None:
        """Mark the player as no longer alive.

        Returns:
            None.
        """
        self.alive = False

    def lose_life(self) -> None:
        """Remove a life and end the game when none remain.

        Returns:
            None.
        """
        if self.lives > 0:
            self.lives -= 1
        if self.lives <= 0:
            self.dead()

    def add_life(self) -> None:
        """Grant one extra life.

        Returns:
            None.
        """
        self.lives += 1

    def activate_power(self) -> None:
        """Start or refresh the power-pellet effect.

        Returns:
            None.
        """
        self.powered_up = True
        self.power_start_time = pygame.time.get_ticks()

    def toggle_invincibility(self) -> None:
        """Toggle the evaluation invincibility cheat.

        Returns:
            None.
        """
        self.invincible = not self.invincible

    def update_power(self) -> None:
        """Expire power after its configured duration.

        Returns:
            None.
        """
        if self.powered_up:
            if (
                pygame.time.get_ticks() - self.power_start_time
                >= self.power_duration
            ):
                self.powered_up = False

    def move(self, maze: "Maze") -> None:
        """Move toward the next allowed tile.

        Args:
            maze: Current maze and its coordinate conversion helpers.

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

    def draw(self, screen: pygame.Surface) -> None:
        """Render this actor or uneaten pellet.

        Args:
            screen: Surface used to display or draw the game.

        Returns:
            None.
        """
        image = self.images[self.direction]
        rect = image.get_rect(center=(self.x, self.y))
        screen.blit(image, rect)
