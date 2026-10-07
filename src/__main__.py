import sys
import time

import pygame

from .game.game import Game
from .game.ghost import GhostsManager
from .game.player import Player
from .maze import Maze
from .parsing import Parser
from .ui import Draw

try:
    if len(sys.argv) != 2:
        raise Exception("U should add just Arg")
    parser = Parser(sys.argv[1])
    level = 0
    maze = Maze(parser.parser(), level)
    screen = maze.screen
    tim = time.monotonic()
    time_mode_delay = 0.3

    clock = pygame.time.Clock()

    player = Player(
        5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
        5 * maze.CELL_SIZE + maze.CELL_SIZE // 2,
        10,
        maze.WI,
        maze.HE,
    )
    draw = Draw(screen)
    game = Game(screen, maze.WI, maze.HE)
    ghosts = GhostsManager(draw, maze)
    ghosts.create_ghost(10, 22, 32, (1, 2))
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
        player_grid = maze.pixel_to_grid(player.x, player.y)
        ghosts.move_all(maze, player_grid)
        ghosts.draw_all()

        pygame.display.flip()
        clock.tick(60)
except Exception as e:
    print(e)
