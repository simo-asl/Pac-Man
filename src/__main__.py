import sys

import pygame

from .maze import Maze
from .game.game import Game
from .game.player import Player


maze = Maze()
screen = maze.screen

clock = pygame.time.Clock()


player = Player(
    5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
    5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
    10,
    maze.WI,
    maze.HE
)

game = Game(screen, maze.WI, maze.HE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.move(maze)
    player.update_power()

    screen.fill((0, 0, 0))
    maze.draw_maze()

    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)
