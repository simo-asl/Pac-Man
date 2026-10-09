from collections import deque

from pygame import Surface

from ..maze import Maze
from ..ui import Draw


class Ghost:
    def __init__(
        self,
        x: int,
        y: int,
        maze: Maze,
        draw: Draw,
        direction: int,
        corner: tuple[int, int],
        kind: str,
        speed: int = 2,
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.corner = corner
        self.kind = kind
        self.mode = "chase"
        self.edible = False
        self.alive = True
        self.speed = speed
        self.images = {
            "blinky": "assets/blinky.png",
            "pinky": "assets/pinky.png",
            "inky": "assets/inky.png",
            "clyde": "assets/clyde.png",
        }
        self.maze = maze
        self.draw = draw
        self.load: Surface = draw.load_image(f"src/game/{self.images[self.kind]}")
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(x, y)
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.target_x, self.target_y = self.maze.grid_to_pixel(x, y)

    def draw_ghost(self) -> None:
        x = self.pixel_x - self.load.get_width() // 2
        y = self.pixel_y - self.load.get_height() // 2
        self.draw.draw_image(self.load, x, y)

    def update(self) -> None:
        if self.pixel_x < self.target_x:
            self.pixel_x = min(self.speed + self.pixel_x, self.target_x)
        elif self.pixel_x > self.target_x:
            self.pixel_x = max(self.pixel_x - self.speed, self.target_x)

        if self.pixel_y < self.target_y:
            self.pixel_y = min(self.pixel_y + self.speed, self.target_y)
        elif self.pixel_y > self.target_y:
            self.pixel_y = max(self.pixel_y - self.speed, self.target_y)

    def is_at_target(self) -> bool:
        return self.pixel_x == self.target_x and self.pixel_y == self.target_y


class GhostsManager:
    def __init__(self, draw: Draw, maze: Maze) -> None:
        self.ghosts: list[Ghost] = []
        self.draw = draw
        self.maze = maze

    def create_ghost(
        self,
        x: int,
        y: int,
        direction: int,
        corner: tuple[int, int],
        kind: str = "blinky",
        speed: int = 2,
    ) -> None:
        ghost = Ghost(x, y, self.maze, self.draw, direction, corner, kind, speed)
        self.ghosts.append(ghost)

    def find_path_to_player(
        self, maze: Maze, player_pos: tuple[int, int], ghost: Ghost
    ) -> list[tuple[int, int]]:
        start_x, start_y = ghost.x, ghost.y
        q: deque = deque()
        parents = {}
        visited = set()
        visited.add((start_x, start_y))
        q.append((start_x, start_y))
        while q:
            curr = q.popleft()
            if curr == player_pos:
                path = []
                while curr != (start_x, start_y):
                    path.append(curr)
                    curr = parents[curr]
                path.reverse()
                return path
            for n in maze.get_available_moves(curr[0], curr[1]):
                if n in visited:
                    continue
                parents[n] = curr
                visited.add(n)
                q.append(n)

        return []

    def move_ghost(
        self,
        ghost: Ghost,
        maze: Maze,
        player_pos: tuple[int, int],
    ) -> None:
        path = []
        if ghost.kind == "blinky":
            path = self.find_path_to_player(maze, player_pos, ghost)
        elif ghost.kind == "pinky":
            ...
        elif ghost.kind == "inky":
            ...
        elif ghost.kind == "clyde":
            pass
        if not path:
            return
        ghost.move(*path[0])

    def move_all(
        self,
        maze: Maze,
        player_pos: tuple[int, int],
    ) -> None:
        for ghost in self.ghosts:
            if not ghost.is_at_target():
                continue
            self.move_ghost(ghost, maze, player_pos)

    def draw_all(self):
        for ghost in self.ghosts:
            ghost.update()
            ghost.draw_ghost()
