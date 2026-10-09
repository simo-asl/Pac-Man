import math

from pygame import Surface

from ..maze import DIRECTIONS, Maze
from ..ui import Draw
from .player import Player


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
    def __init__(self, draw: Draw, maze: Maze, player: Player) -> None:
        self.ghosts: list[Ghost] = []
        self.draw = draw
        self.maze = maze
        self.player = player

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

    def choose_next_tile(
        self,
        ghost: Ghost,
        target: tuple[int, int],
    ) -> tuple[int, int] | None:
        moves = self.maze.get_available_moves(ghost.x, ghost.y)
        dx, dy = DIRECTIONS[ghost.direction]
        reverse = (ghost.x - dx, ghost.y - dy)
        forward_moves = [pos for pos in moves if pos != reverse]
        if not forward_moves:
            return reverse if reverse in moves else None
        res = {}
        for x, y in forward_moves:
            edisition_formuala = math.sqrt((target[0] - x) ** 2 + (target[1] - y) ** 2)
            res[(x, y)] = edisition_formuala
        best_pos = min(res, key=lambda pos: res[pos])
        return best_pos

    def get_pinky_target(
        self, player_pos: tuple[int, int], player_direction: int
    ) -> tuple[int, int]:

        x, y = player_pos
        dx, dy = DIRECTIONS[player_direction]
        for distance in range(4, -1, -1):
            tx = x + dx * distance
            ty = y + dy * distance
            if self.maze.is_inside(tx, ty):
                return tx, ty
        return player_pos

    def get_inky_target(
        self,
        player_pos: tuple[int, int],
        player_direction: int,
        blinky_pos: tuple[int, int],
    ) -> tuple[int, int]:
        x, y = player_pos
        dx, dy = DIRECTIONS[player_direction]
        for distance in range(2, -1, -1):
            tx = x + dx * distance
            ty = y + dy * distance
            if self.maze.is_inside(tx, ty):
                target_two = tx, ty
                break

        target_x = 2 * target_two[0] - blinky_pos[0]
        target_y = 2 * target_two[1] - blinky_pos[1]
        return target_x, target_y

    def move_ghost(
        self,
        ghost: Ghost,
    ) -> None:
        player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
        if ghost.kind == "blinky":
            target = player_pos
        elif ghost.kind == "pinky":
            target = self.get_pinky_target(player_pos, self.player.direction)
        elif ghost.kind == "inky":
            blinky = next((g for g in self.ghosts if g.kind == "blinky"), None)
            if blinky is None:
                return
            target = self.get_inky_target(
                player_pos, self.player.direction, (blinky.x, blinky.y)
            )
        elif ghost.kind == "clyde":
            distance_square = (ghost.x - player_pos[0]) ** 2 + (
                ghost.y - player_pos[1]
            ) ** 2
            if distance_square >= 64:
                target = player_pos
            else:
                target = ghost.corner
        best_pos = self.choose_next_tile(ghost, target)
        if not best_pos:
            return
        dx = best_pos[0] - ghost.x
        dy = best_pos[1] - ghost.y
        for dire, vect in DIRECTIONS.items():
            if (dx, dy) == vect:
                ghost.direction = dire
                break
        ghost.move(*best_pos)

    def move_all(
        self,
    ) -> None:
        for ghost in self.ghosts:
            if not ghost.is_at_target():
                continue
            self.move_ghost(ghost)

    def draw_all(self):
        for ghost in self.ghosts:
            ghost.update()
            ghost.draw_ghost()
