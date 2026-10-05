import sys

import pygame

from .parsing import Parser
from .game.game import Game
from .game.player import Player
from .maze import Maze

try:
    if len(sys.argv) != 2:
        raise Exception("U should add just Arg")
    parser = Parser(sys.argv[1])
    level = 0
    maze = Maze(parser.parser(), level)
    screen = maze.screen

    clock = pygame.time.Clock()

    player = Player(
        5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
        5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
        10,
        maze.WI,
        maze.HE,
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
except Exception as e:
    print(e)
