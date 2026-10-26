"""Define normal and power pellets."""

from ..ui import Draw


class Pacgum:

    """Represent an edible pellet with a position and point value.
    """
    def __init__(
        self, x: int, y: int, radius: int, points: int = 10
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            radius: Radius in pixels used for drawing or collision checks.
            points: Nonnegative score value awarded for this item or game.

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
        """Mark the pellet or ghost as eaten.

        Returns:
            None.
        """
        self.eaten = True

    def draw(self, draw: Draw) -> None:
        """Draw this actor or its uneaten pellet through the drawing helper.

        Args:
            draw: Drawing helper used to prepare or display game images.

        Returns:
            None.
        """
        if not self.eaten:
            draw.draw_circle(self.x, self.y, self.radius, self.color)


class SuperPacgum(Pacgum):

    """Represent a larger pellet that grants temporary power.
    """
    def __init__(self, x: int, y: int, radius: int, points: int = 50) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            points: Nonnegative score value awarded for this item or game.

        Returns:
            None.
        """
        super().__init__(x, y, radius, points)
