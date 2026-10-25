"""Coordinate ghost paths, frightened behavior and rendering."""

from collections import deque
import time

from ..maze import DIRECTIONS, Maze
from ..ui import Draw
from .ghost import Ghost
from .player import Player


class GhostsManager:
    """Coordinate ghost behavior and collision checks."""

    def __init__(self, draw: Draw, maze: Maze, player: Player) -> None:
        """Initialize this object and its dependencies.

        Args:
            draw: Drawing helper for the target surface.
            maze: Current maze and its coordinate conversion helpers.
            player: Player whose position, lives or power state is used.

        Returns:
            None.
        """
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
        speed: float = Ghost.BASE_SPEED,
    ) -> None:
        """Create and register a ghost at its corner.

        Args:
            x: Column of the maze cell.
            y: Row of the maze cell.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8 left.
            corner: Home corner as a pair of maze column and row indices.
            kind: Ghost name used to select its appearance and chase behavior.
            speed: Movement speed in tiles per second.

        Returns:
            None.
        """
        ghost = Ghost(
            x, y, self.maze, self.draw, direction, corner, kind, speed
        )
        self.ghosts.append(ghost)

    def choose_next_tile(
        self,
        ghost: Ghost,
        target: tuple[int, int],
    ) -> tuple[int, int] | None:
        """Follow a shortest open path instead of circling blocked walls.

        Args:
            ghost: Ghost whose movement or collision is being evaluated.
            target: Desired destination as a maze column and row.

        Returns:
            tuple[int, int] | None: First cell on a shortest route, or None at
                the destination.
        """
        start = (ghost.x, ghost.y)
        if start == target:
            return None
        queue = deque([start])
        first_steps: dict[tuple[int, int], tuple[int, int] | None] = {
            start: None,
        }
        closest = start
        while queue:
            position = queue.popleft()
            if position == target:
                return first_steps[position]
            if (position[0] - target[0]) ** 2 + (
                position[1] - target[1]
            ) ** 2 < (closest[0] - target[0]) ** 2 + (
                closest[1] - target[1]
            ) ** 2:
                closest = position
            for neighbor in self.maze.get_available_moves(*position):
                if neighbor in first_steps:
                    continue
                first_steps[neighbor] = (
                    neighbor if position == start else first_steps[position]
                )
                queue.append(neighbor)
        # Ambush targets can be outside the grid or inside the solid pattern.
        return first_steps[closest]

    def get_pinky_target(
        self, player_pos: tuple[int, int], player_direction: int
    ) -> tuple[int, int]:
        """Aim ahead of the player without leaving the maze.

        Args:
            player_pos: Player position as a maze column and row.
            player_direction: Player direction wall bit.

        Returns:
            tuple[int, int]: A target cell ahead of the player and inside the
                maze.
        """
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
        """Compute the ambush target relative to Blinky.

        Args:
            player_pos: Player position as a maze column and row.
            player_direction: Player direction wall bit.
            blinky_pos: Blinky position used as an ambush reference.

        Returns:
            tuple[int, int]: The ambush cell reflected around the Blinky
                reference.
        """
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
        """Flee by open-path distance, waiting when a dead end is safest.

        Args:
            ghost: Ghost whose movement or collision is being evaluated.

        Returns:
            tuple[int, int] | None: A cell farther from the player, or None at
                a dead end.
        """
        player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
        distances = {player_pos: 0}
        queue = deque([player_pos])
        while queue:
            position = queue.popleft()
            for neighbor in self.maze.get_available_moves(*position):
                if neighbor not in distances:
                    distances[neighbor] = distances[position] + 1
                    queue.append(neighbor)
        current = (ghost.x, ghost.y)
        moves = self.maze.get_available_moves(*current)
        if not moves:
            return None
        best = max(moves, key=lambda pos: distances.get(pos, -1))
        if distances.get(best, -1) <= distances.get(current, -1):
            return None
        return best

    def is_collision(self, ghost: Ghost) -> bool:
        """Return whether the ghost and player overlap.

        Args:
            ghost: Ghost whose movement or collision is being evaluated.

        Returns:
            bool: True when the player and ghost collision circles overlap.
        """
        dx = self.player.x - ghost.pixel_x
        dy = self.player.y - ghost.pixel_y
        colleesion_radis = self.player.radius + ghost.radius

        return dx * dx + dy * dy <= colleesion_radis**2

    def move_ghost(
        self,
        ghost: Ghost,
    ) -> None:
        """Choose a next tile for the current ghost mode.

        Args:
            ghost: Ghost whose movement or collision is being evaluated.

        Returns:
            None.
        """
        if ghost.mode == "chase":
            player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
            if ghost.kind == "blinky":
                target = player_pos
            elif ghost.kind == "pinky":
                target = self.get_pinky_target(
                    player_pos, self.player.direction
                )
            elif ghost.kind == "inky":
                blinky = next(
                    (g for g in self.ghosts if g.kind == "blinky"), None
                )
                if blinky is None:
                    return
                target = self.get_inky_target(
                    player_pos, self.player.direction, (blinky.x, blinky.y)
                )
            else:
                target = player_pos
            distance = abs(ghost.x - player_pos[0]) + abs(
                ghost.y - player_pos[1]
            )
            if (
                distance <= 4
                or not self.maze.is_inside(*target)
                or not self.maze.get_available_moves(*target)
            ):
                target = player_pos
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
        """Choose targets for ghosts that are ready to move.

        Returns:
            None.
        """
        if self.frozen:
            return
        for ghost in self.ghosts:
            if not ghost.is_at_target():
                continue
            self.move_ghost(ghost)

    def draw_all(self) -> None:
        """Render every ghost.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            ghost.draw_ghost()

    def update_all(self, delta_time: float = 1 / 60) -> None:
        """Advance ghosts unless the freeze cheat is active.

        Args:
            delta_time: Elapsed active-frame time in seconds.

        Returns:
            None.
        """
        if self.frozen:
            return
        for ghost in self.ghosts:
            ghost.update(delta_time)

    def frighten_all(self) -> None:
        """Switch uneaten ghosts to their frightened mode.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            if ghost.mode != "eaten":
                ghost.mode = "frightened"

    def restore_all(self) -> None:
        """Return frightened ghosts to chase mode.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            if ghost.mode == "frightened":
                ghost.mode = "chase"
