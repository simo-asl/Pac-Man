import math
import random
import time

from ..maze import DIRECTIONS, Maze
from ..ui import Draw
from .ghost import Ghost
from .player import Player


class GhostsManager:
    def __init__(self, draw: Draw, maze: Maze, player: Player) -> None:
        self.ghosts: list[Ghost] = []
        self.draw = draw
        self.maze = maze
        self.player = player
        self.frozen = False

    def create_ghost(
        self,
        x: int,
        y: int,
        direction: int,
        corner: tuple[int, int],
        kind: str = "blinky",
        speed: int = 2,
    ) -> None:
        ghost = Ghost(x, y, self.maze, self.draw, direction,
                      corner, kind, speed)
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
            edisition_formuala = math.sqrt(
                (target[0] - x) ** 2 + (target[1] - y) ** 2)
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

    def choose_frightened_tile(
        self,
        ghost: Ghost,
    ) -> tuple[int, int] | None:
        moves = self.maze.get_available_moves(ghost.x, ghost.y)
        dx, dy = DIRECTIONS[ghost.direction]
        reverse = (ghost.x - dx, ghost.y - dy)
        new_moves = [move for move in moves if move != reverse]
        if not new_moves:
            return reverse if reverse in moves else None
        player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
        return max(
            new_moves,
            key=lambda pos: (
                (pos[0] - player_pos[0]) ** 2 + (pos[1] - player_pos[1]) ** 2
            ),
        )

    def is_collesion(self, ghost: Ghost) -> bool:
        dx = self.player.x - ghost.pixel_x
        dy = self.player.y - ghost.pixel_y
        colleesion_radis = self.player.radius + 10

        return dx * dx + dy * dy <= colleesion_radis**2

    def move_ghost(
        self,
        ghost: Ghost,
    ) -> None:
        if ghost.mode == "chase":
            player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
            if ghost.kind == "blinky":
                target = player_pos
            elif ghost.kind == "pinky":
                target = self.get_pinky_target(
                    player_pos, self.player.direction)
            elif ghost.kind == "inky":
                blinky = next(
                    (g for g in self.ghosts if g.kind == "blinky"), None)
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
        elif ghost.mode == "frightened":
            best_pos = self.choose_frightened_tile(ghost)
        elif ghost.mode == "eaten":
            if time.monotonic() - ghost.time_eaten >= 5:
                ghost.respawn()
                return
            best_pos = self.choose_next_tile(ghost, ghost.spawn)
        if best_pos is None:
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

        if self.frozen:
            return
        for ghost in self.ghosts:
            if not ghost.is_at_target():
                continue
            self.move_ghost(ghost)

    def draw_all(self):
        for ghost in self.ghosts:
            ghost.draw_ghost()

    def update_all(self):
        if self.frozen:
            return
        for ghost in self.ghosts:
            ghost.update()

    def frighten_all(self) -> None:
        for ghost in self.ghosts:
            if ghost.mode != "eaten":
                ghost.mode = "frightened"

    def restore_all(self) -> None:
        for ghost in self.ghosts:
            if ghost.mode == "frightened":
                ghost.mode = "chase"
