"""Coordinate ghost navigation and edible states."""

import time
from collections import deque

from ..maze import DIRECTIONS, Maze
from ..ui import Draw
from .ghost import Ghost
from .player import Player


class GhostsManager:
    """Coordinate ghost targets, movement and power states."""

    def __init__(self, draw: Draw, maze: Maze, player: Player) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            draw: Drawing helper used to prepare or display game images.
            maze: Current maze with walls and grid-to-pixel conversion
                helpers.
            player: Player whose lives, position or power state is used.

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
        speed: int = 2,
    ) -> None:
        """Create and register a ghost at the supplied grid position.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            direction: Direction wall bit: 1 up, 2 right, 4 down, or 8
                left.
            corner: Grid coordinates of the ghost home corner.
            kind: Ghost sprite name.
            speed: Distance moved in pixels on each gameplay update.

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
        """Use BFS to find the first step on a shortest path to the target.

        Args:
            ghost: Ghost whose position, mode or destination is being
                processed.
            target: Grid coordinates toward which the ghost should move.

        Returns:
            Next route cell, or None if at the target or it is unreachable.
        """
        start = (ghost.x, ghost.y)
        if start == target:
            return None
        queue = deque([start])
        parents: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while queue:
            current = queue.popleft()
            if current == target:
                step = current
                while parents[step] != start:
                    parent = parents[step]
                    assert parent is not None
                    step = parent
                return step
            for neighbor in self.maze.get_available_moves(*current):
                if neighbor not in parents:
                    parents[neighbor] = current
                    queue.append(neighbor)
        return None

    def choose_frightened_tile(
        self,
        ghost: Ghost,
    ) -> tuple[int, int] | None:
        """Choose a legal neighbor farthest from the player.

        Args:
            ghost: Ghost whose position, mode or destination is being
                processed.

        Returns:
            Next grid cell away from the player, or None if blocked.
        """
        moves = self.maze.get_available_moves(ghost.x, ghost.y)
        if not moves:
            return None
        dx, dy = DIRECTIONS[ghost.direction]
        previous = (ghost.x - dx, ghost.y - dy)
        forward_moves = [move for move in moves if move != previous]
        if forward_moves:
            moves = forward_moves
        player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
        return max(
            moves,
            key=lambda pos: (
                (pos[0] - player_pos[0]) ** 2 + (pos[1] - player_pos[1]) ** 2
            ),
        )

    def is_collesion(self, ghost: Ghost) -> bool:
        """Check whether this ghost overlaps the player collision circle.

        Args:
            ghost: Ghost whose position, mode or destination is being
                processed.

        Returns:
            True if the player and ghost collision circles overlap.
        """
        dx = self.player.x - ghost.pixel_x
        dy = self.player.y - ghost.pixel_y
        colleesion_radis = self.player.radius + ghost.radius

        return dx * dx + dy * dy <= colleesion_radis**2

    def move_ghost(
        self,
        ghost: Ghost,
    ) -> None:
        """Choose the next destination according to this ghost mode.

        Args:
            ghost: Ghost whose position, mode or destination is being
                processed.

        Returns:
            None.
        """
        best_pos = None
        if ghost.mode == "chase":
            player_pos = self.maze.pixel_to_grid(self.player.x, self.player.y)
            best_pos = self.choose_next_tile(ghost, player_pos)
        elif ghost.mode == "frightened":
            best_pos = self.choose_frightened_tile(ghost)
        elif ghost.mode == "eaten":
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
        """Choose destinations for ghosts that reached their targets.

        Returns:
            None.
        """
        if self.frozen:
            return
        for ghost in self.ghosts:
            if (
                ghost.mode == "eaten"
                and time.monotonic() - ghost.time_eaten >= 5
            ):
                ghost.respawn()
                if self.player.powered_up:
                    ghost.mode = "frightened"
                continue
            if not ghost.is_at_target():
                continue
            self.move_ghost(ghost)

    def draw_all(self) -> None:
        """Draw every ghost using its current mode and direction.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            ghost.draw_ghost()

    def update_all(self) -> None:
        """Advance ghost positions unless the freeze cheat is active.

        Returns:
            None.
        """
        if self.frozen:
            return
        for ghost in self.ghosts:
            ghost.update()

    def frighten_all(self) -> None:
        """Make every uneaten ghost edible while player power is active.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            if ghost.mode != "eaten":
                ghost.mode = "frightened"

    def restore_all(self) -> None:
        """Restore frightened ghosts to their normal chase behavior.

        Returns:
            None.
        """
        for ghost in self.ghosts:
            if ghost.mode == "frightened":
                ghost.mode = "chase"
