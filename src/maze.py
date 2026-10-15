import pygame
from mazegenerator import MazeGenerator

from .parsing import GameConfig
from .ui import Draw

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
    def __init__(self, config: GameConfig, level: int):
        """ ""
        Maze: class for Creating the maze and drawing it
        Args:
            config: Config class that carry the configs.
            level: Level of the Game.
        """
        pygame.init()
        # Dementions just for try my part
        # feel free to change them since this is ur part
        self.CELL_SIZE = 30
        self.columns = config.levels[level].width
        self.rows = config.levels[level].height

        self.WI = self.columns * self.CELL_SIZE
        self.HE = self.rows * self.CELL_SIZE

        self.screen = pygame.display.set_mode((self.WI, self.HE))
        pygame.display.set_caption("Pac-Man")

        if level == 0:
            self.maze_init = MazeGenerator((self.columns, self.rows), seed=42)
        elif config.levels[level].seed is not None:
            self.maze_init = MazeGenerator(
                (self.columns, self.rows), seed=config.levels[level].seed
            )
        else:
            self.maze_init = MazeGenerator((self.columns, self.rows))
        self.maze = self.maze_init.maze

        self.draw = Draw(self.screen, self.CELL_SIZE)

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

    def is_inside(self, x: int, y: int) -> bool:
        """Func for Checking if the cordinate inside the
            maze

        Args:
            x: the corddinate x.
            y: the cordinate y.

        Returns:
            return true if its inside the maze False if not.
        """
        return 0 <= x < self.columns and 0 <= y < self.rows

    def can_move(self, x: int, y: int, direction: int) -> bool:
        """Check if its possible to Move into that Direction

        Args:
            x: corddinate of x.
            y: corddinate of y.
            direction: Direction.

        Returns:
            True if can move into that dir false if nah.
        """
        if not self.is_inside(x, y):
            return False
        return not (self.maze[y][x] & direction)

    # U should give me this method but u didn't to let me see the fkn maze
    # this methode same as run_ui
    def draw_maze(self) -> None:
        """Draw the Maze"""
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(x, y, cell, color38, 2)

    def get_available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        paths = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x = x + dx
            new_y = y + dy
            if self.can_move(x, y, direction) and self.is_inside(new_x, new_y):
                paths.append((new_x, new_y))

        return paths

    def grid_to_pixel(self, x: int, y: int) -> tuple[int, int]:
        return (
            x * self.CELL_SIZE + self.CELL_SIZE // 2,
            y * self.CELL_SIZE + self.CELL_SIZE // 2,
        )

    def pixel_to_grid(self, x: int, y: int) -> tuple[int, int]:
        return (x // self.CELL_SIZE, y // self.CELL_SIZE)

    # We need this method to get the center pos if each walkable cell
    # So Game can place pacgums bla depending on Maze internals
    def get_walkable_positions(self) -> list[tuple[int, int]]:
        postions = []
        for row_idx, row in enumerate(self.maze):
            for col_idx, value in enumerate(row):
                if value == 15:
                    continue
                center_x, center_y = self.grid_to_pixel(col_idx, row_idx)
                postions.append((center_x, center_y))

        return postions


