from ..ui import Draw


class Pacgum:

    def __init__(
        self, x: int, y: int, radius: int, points: int = 10
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.color: tuple = (255, 255, 255)
        self.radius: int = radius
        self.points: int = points
        self.eaten: bool = False

    def get_eaten(self) -> None:
        self.eaten = True

    def draw(self, draw: Draw) -> None:
        if not self.eaten:
            draw.draw_circle(self.x, self.y, self.radius, self.color)


class SuperPacgum(Pacgum):

    def __init__(self, x: int, y: int, points: int = 50) -> None:
        super().__init__(x, y, 7, points)
