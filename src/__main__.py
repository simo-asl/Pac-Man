import sys
import time

import pygame

from .game.game import Game
from .game.ghost_manger import GhostsManager
from .game.player import Player
from .maze import Maze
from .parsing import Parser
from .ui import Draw

try:
    if len(sys.argv) != 2:
        raise Exception("U should add just Arg")
    parser = Parser("config.json")
    level = 0
    config = parser.parser()
    maze = Maze(config, level)

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
        lives=config.lives,
    )
    player_spawn = (player.x, player.y)
    draw = Draw(screen)
    game = Game(screen, maze.WI, maze.HE, config=config)
    positions = maze.get_walkable_positions()
    corners = [positions[0], positions[maze.columns - 1],
               positions[-maze.columns], positions[-1]]
    for corner in corners:
        if corner in positions:
            positions.remove(corner)
    if player_spawn in positions:
        positions.remove(player_spawn)

    pacgums = game.create_pacgums(positions)
    superpacgums = game.create_superpac(corners)
    ghosts = GhostsManager(draw, maze, player)
    ghosts.create_ghost(
        10,
        22,
        2,
        (maze.columns - 1, 0),
        "blinky",
    )

    ghosts.create_ghost(
        1,
        2,
        2,
        (0, 0),
        "pinky",
    )

    ghosts.create_ghost(
        14,
        14,
        1,
        (maze.columns - 1, maze.rows - 1),
        "inky",
    )

    ghosts.create_ghost(
        1,
        maze.rows - 2,
        2,
        (0, maze.rows - 1),
        "clyde",
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update_death(player, ghosts)
        if game.level_time_remaining() == 0:
            player.dead()

        if not game.paused and player.alive:
            player.move(maze)
            player.update_power()

            if player.powered_up:
                ghosts.frighten_all()
            else:
                ghosts.restore_all()

            ghosts.move_all()
            game.check_all_collisions(
                player, superpacgums, pacgums, ghosts
            )
            ghosts.update_all()

        screen.fill((0, 0, 0))
        maze.draw_maze()

        for pacgum in pacgums:
            pacgum.draw(screen)

        for superpac in superpacgums:
            superpac.draw(screen)

        player.draw(screen)
        ghosts.draw_all()

        pygame.display.flip()
        clock.tick(60)
except Exception as e:
    print(e)
