"""Represent normal and power pellets."""

from ..ui import Draw


class Pacgum:
    """Represent a collectible score pellet."""

    def __init__(self, x: int, y: int, radius: int, points: int = 10) -> None:
        """Initialize this object and its dependencies.

        Args:
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.
            radius: Radius in pixels for drawing or collision detection.
            points: Non-negative number of points awarded or stored.

        Returns:
            None.
        """
        self.x: int = x
        self.y: int = y
        self.color: tuple = (255, 255, 255)
        self.radius: int = radius
        self.points: int = points
        self.eaten: bool = False

    def get_eaten(self) -> None:
        """Mark this item or ghost as eaten.

        Returns:
            None.
        """
        self.eaten = True

    def draw(self, draw: Draw) -> None:
        """Render this actor or uneaten pellet.

        Args:
            draw: Drawing helper for the target surface.

        Returns:
            None.
        """
        if not self.eaten:
            draw.draw_circle(self.x, self.y, self.radius, self.color)


class SuperPacgum(Pacgum):
    """Represent a power pellet."""

    def __init__(self, x: int, y: int, points: int = 50) -> None:
        """Initialize this object and its dependencies.

        Args:
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.
            points: Non-negative number of points awarded or stored.

        Returns:
            None.
        """
        super().__init__(x, y, 7, points)
