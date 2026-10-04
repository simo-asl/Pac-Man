from .draw import Draw

from mazegenerator import MazeGenerator
import pygame

color38 = (255, 153, 204)
color39 = (204, 153, 255)
color40 = (255, 204, 153)


class Maze:
    def __init__(self):
        self.CELL_SIZE = 20
        pygame.init()
        self.runing = True
        self.WI = 800
        self.HE = 600
        self.screen = pygame.display.set_mode((self.WI, self.HE))
        self.columns = self.WI // self.CELL_SIZE
        self.rows = self.HE // self.CELL_SIZE
        self.maze_init = MazeGenerator((self.columns, self.rows))
        self.maze = self.maze_init.maze

        self.draw = Draw(self.screen)

    def run_ui(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(x, y, cell, color38, 4)
        runing = True
        while runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False

            pygame.display.flip()

    def can_move(self, x: int, y: int, direction: int) -> bool:
        return not (self.maze[y][x] & direction)

    def get_available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        paths = []
        if self.can_move(x, y, 1):
            paths.append((x, y - 1))
        if self.can_move(x, y, 2):
            paths.append((x + 1, y))
        if self.can_move(x, y, 4):
            paths.append((x, y + 1))
        if self.can_move(x, y, 8):
            paths.append((x - 1, y))

        return paths


t = Maze()
t.run_ui()
