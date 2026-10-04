import mazegenerator
import pygame
from mazegenerator import MazeGenerator


CELL_SIZE = 24
MAZE_SIZE = (21, 21)
WALL_COLOR = (39, 91, 220)
BACKGROUND_COLOR = (10, 10, 24)


maze = MazeGenerator(MAZE_SIZE)
print(maze.maze)


def can_move(maze: MazeGenerator, x: int, y: int) -> bool: ...
