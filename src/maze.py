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


t = Maze()
t.run_ui()
