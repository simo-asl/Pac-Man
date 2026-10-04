from mazegenerator import MazeGenerator
import pygame


def draw_horizontal_line(scren, start_x: int, y: int, end_x: int, color):
    for x in range(start_x, end_x):
        scren.set_at((x, y), color)


def draw_vertical_line(scren, x: int, start_y: int, end_y: int, color):
    for y in range(start_y, end_y):
        scren.set_at((x, y), color)


def draw_maze(scren, cell_x, cell_y, cell, color):
    x = cell_x * CELL_SIZE
    y = cell_y * CELL_SIZE
    x2 = x + CELL_SIZE
    y2 = y + CELL_SIZE
    if cell & 1:
        draw_horizontal_line(scren, x, y, x2, color)
    if cell & 2:
        draw_vertical_line(scren, x2, y, y2, color)
    if cell & 4:
        draw_horizontal_line(scren, x, y2, x, color)
    if cell & 8:
        draw_vertical_line(scren, x, y2, x2, color)


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
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            draw_maze(screen, x, y, cell, WHITE)
    pygame.display.flip()
