from mazegenerator import MazeGenerator
import pygame


class Draw:
    def __init__(self, scren):
        self.scren = scren

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int, color, thickness=1
    ):
        for offset in range(thickness):
            for x in range(start_x, end_x):
                self.scren.set_at((x, y + offset), color)

    def draw_vertical_line(self, x: int, start_y: int, end_y: int, color, thickness=1):
        for offset in range(thickness):
            for y in range(start_y, end_y):
                self.scren.set_at((x + offset, y), color)

    def draw_maze(self, cell_x, cell_y, cell, color, thickness=1):
        x = cell_x * CELL_SIZE
        y = cell_y * CELL_SIZE
        x2 = x + CELL_SIZE
        y2 = y + CELL_SIZE
        if cell & 1:
            self.draw_horizontal_line(x, y, x2, color, thickness)
        if cell & 2:
            self.draw_vertical_line(x2, y, y2, color, thickness)
        if cell & 4:
            self.draw_horizontal_line(x, y2, x, color, thickness)
        if cell & 8:
            self.draw_vertical_line(x, y2, x2, color, thickness)


CELL_SIZE = 30
WHITE = (255, 255, 255)
pygame.init()
runing = True
WI = 1000
HE = 1500
screen = pygame.display.set_mode((WI, HE))
columns = WI // CELL_SIZE
rows = HE // CELL_SIZE
maze_init = MazeGenerator((columns, rows))
maze = maze_init.maze
draw = Draw(screen)
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            draw.draw_maze(x, y, cell, WHITE, 4)
    pygame.display.flip()
