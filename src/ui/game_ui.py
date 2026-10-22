import pygame

from ..game import Game, Player
from ..maze import Maze
from .draw import Draw


class GameUi:
    def __init__(self, draw: Draw, player: Player, game: Game, maze: Maze):
        self.draw = draw
        self.player = player
        self.game = game
        self.height = self.draw.screen.get_height()
        self.maze = maze
        self.width = self.draw.screen.get_width()
        self.cache = {}

    def menu_game(self, thinkeess: int = 5):
        offset_x = getattr(self.maze, "offset_x", (self.width - self.maze.WI) // 2)

        offset_y = getattr(self.maze, "offset_y", (self.height - self.maze.HE) // 2)
        if not self.cache.get(self.maze.level, None):
            t = pygame.Surface((self.width, self.height))
            surface_draw = Draw(t)
            for y, row in enumerate(self.maze.maze):
                for x, cell in enumerate(row):
                    surface_draw.draw_maze(
                        x,
                        y,
                        cell,
                        (255, 220, 50),
                        self.maze.CELL_SIZE,
                        thinkeess,
                        offset_x,
                        offset_y,
                    )
            self.cache[self.maze.level] = t

        self.draw.screen.fill((0, 0, 0))
        self.draw.draw_image(self.cache[self.maze.level], 0, 0)
        self.draw.draw_text(
            f"Level: {self.maze.level}",
            int((self.width // 5) * 4),
            25,
            80,
            (255, 220, 50),
        )
        self.draw.draw_text(
            f"Life: {self.player.lives}",
            int((self.width // 5) * 0.5),
            25,
            80,
            (255, 220, 50),
        )
        self.draw.draw_text(
            f"Score: {self.game.score}",
            int((self.width // 5) * 0.5),
            self.height - 70,
            80,
            (255, 220, 50),
        )
