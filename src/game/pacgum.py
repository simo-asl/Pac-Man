import pygame
from ..ui import Draw


# To add PacGums, we need the get_walkable_positions() method from Maze
# It will give me a list of positions where PacGums can be placed
# From that list, I can remove positions that must stay empty
# such as the player's spawn position
#
# SuperPacGums are different: according to the subject, we need exactly
# four of them, placed in the four corners of the maze
#
# Maybe my plan isn't perfect, but at least I'm trying
# Btw, I ended up writing more comments than code hhhhhhhhhhhhh
class Pacgum:

    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x: int = x
        self.y: int = y
        self.color: tuple = (255, 255, 255)
        self.radius: int = radius
        self.points: int = 10
        self.eaten: bool = False

    def get_eaten(self) -> None:
        self.eaten = True

    def draw(self, screen: pygame.Surface) -> None:
        if not self.eaten:
            draw = Draw(screen)
            draw.draw_circle(self.x, self.y, self.radius, self.color)

class SuperPacgum(Pacgum):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)
        self.points = 50
