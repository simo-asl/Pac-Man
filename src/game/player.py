"""Control player movement, lives and temporary power."""

from typing import TYPE_CHECKING
from math import cos, radians, sin
from time import monotonic

import pygame

from .clock import now_ms

if TYPE_CHECKING:
    from ..maze import Maze
    from ..ui.draw import Draw


class Player:
    """Track player movement, lives, power and invincibility.
    """
    MOUTH_FRAME_MS = 70
    MOUTH_ANGLES = (100, 64, 42, 64, 100)
    REST_FRAME = 2

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
        self.images: dict[int, list[pygame.Surface]] = {}
        self.mouth_frame = self.REST_FRAME
        self.last_mouth_frame = monotonic()

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
        self.power_start_time = now_ms()

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
            if (now_ms() - self.power_start_time
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
        previous_position = self.x, self.y
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

        self._update_mouth_animation((self.x, self.y) != previous_position)

    def _mouth_image(
        self, size: tuple[int, int], direction: int, mouth_angle: int,
    ) -> pygame.Surface:
        """Create one bright Pac-Man frame with a transparent mouth wedge."""
        image = pygame.Surface(size, pygame.SRCALPHA)
        center = size[0] // 2, size[1] // 2
        radius = min(size) // 2 - 1
        pygame.draw.circle(image, (247, 185, 54), center, radius)
        pygame.draw.circle(image, (255, 224, 85), center, max(1, radius - 1))
        facing_angle = {1: -90, 2: 0, 4: 90, 8: 180}[direction]
        half_angle = mouth_angle / 2
        mouth_reach = radius * 2
        points = [center]
        for angle in (facing_angle - half_angle, facing_angle + half_angle):
            radians_angle = radians(angle)
            points.append((
                round(center[0] + cos(radians_angle) * mouth_reach),
                round(center[1] + sin(radians_angle) * mouth_reach),
            ))
        pygame.draw.polygon(image, (0, 0, 0, 0), points)
        return image

    def _update_mouth_animation(self, moved: bool) -> None:
        """Advance the mouth from actual movement, rather than drawing.

        Drawing can happen at a different cadence from fixed gameplay updates.
        Advancing here keeps the animation running whenever Pac-Man's pixel
        position changes and leaves rendering as a side-effect-free operation.
        """
        now = monotonic()
        if not moved:
            self.mouth_frame = self.REST_FRAME
            self.last_mouth_frame = now
            return
        elapsed = now - self.last_mouth_frame
        frame_duration = self.MOUTH_FRAME_MS / 1000
        if elapsed >= frame_duration:
            steps = int(elapsed // frame_duration)
            self.mouth_frame = (
                self.mouth_frame + steps
            ) % len(self.MOUTH_ANGLES)
            self.last_mouth_frame += steps * frame_duration

    def draw(self, draw: "Draw") -> None:
        """Draw this actor or its uneaten pellet through the drawing helper.

        Args:
            draw: Drawing helper used to prepare or display game images.

        Returns:
            None.
        """
        if not self.images:
            self.images = {
                direction: [
                    self._mouth_image(
                        (self.radius * 2, self.radius * 2), direction,
                        mouth_angle,
                    )
                    for mouth_angle in self.MOUTH_ANGLES
                ]
                for direction in (1, 2, 4, 8)
            }
        image = self.images[self.direction][self.mouth_frame]
        draw.draw_image(
            image, self.x - image.get_width() // 2,
            self.y - image.get_height() // 2,
        )
