from .ui import Draw

from mazegenerator import MazeGenerator
import pygame

color38 = (255, 153, 204)
color39 = (204, 153, 255)
color40 = (255, 204, 153)

DIRECTIONS = {
    1: (0, -1),  # north
    2: (1, 0),  # east
    4: (0, 1),  # south
    8: (-1, 0),  # west
}


class Maze:
    # Beta layout:
    # The previous version used a fixed 800x600 window and calculated the maze
    # size from it, which created a rectangular maze with unused screen space.
    # For now, we use a square 25x25 maze and calculate the window size from
    # CELL_SIZE so the maze fills the window exactly.
    # These values are manualy intialized for now until we use the conf file
    def __init__(self, seed: int | None = None):
        pygame.init()
        # Dementions just for try my part
        # feel free to change them since this is ur part
        self.CELL_SIZE = 30
        self.columns = 25
        self.rows = 25

        self.WI = self.columns * self.CELL_SIZE
        self.HE = self.rows * self.CELL_SIZE

        self.screen = pygame.display.set_mode(
            (self.WI, self.HE)
        )
        pygame.display.set_caption("Pac-Man")

        if seed is None:
            self.maze_init = MazeGenerator(
                (self.columns, self.rows)
            )
        else:
            self.maze_init = MazeGenerator(
                (self.columns, self.rows),
                seed=seed
            )

        self.maze = self.maze_init.maze

        self.draw = Draw(
            self.screen,
            self.CELL_SIZE
        )

    def run_ui(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(x, y, cell, color38, 2)
        runing = True
        while runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False

            pygame.display.flip()

    def can_move(self, x: int, y: int, direction: int) -> bool:
        return not (self.maze[y][x] & direction)

    # U should give me this method but u didn't to let me see the fkn maze
    def draw_maze(self) -> None:
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(x, y, cell, color38, 2)

    def get_available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        paths = []
        for direction, (dx, dy) in DIRECTIONS.items():
            if self.can_move(x, y, direction):
                paths.append((x + dx, y + dy))

        return paths

    # We need this method to get the center pos if each walkable cell
    # So Game can place pacgums bla depending on Maze internals
    def get_walkable_positions() -> list[tuple[int, int]]:
        pass
