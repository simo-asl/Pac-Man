"""Check shortest routes, legal turns and ghost power states headlessly."""

import unittest
from unittest.mock import patch

import pygame

from src.game.ghost_manger import GhostsManager
from src.game.player import Player
from src.maze import DIRECTIONS, Maze
from src.ui import Draw


class GhostMovementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.maze = Maze.__new__(Maze)
        self.maze.columns = self.maze.rows = 5
        self.maze.CELL_SIZE = 10
        self.maze.offset_x = 17
        self.maze.offset_y = 23
        self.maze.maze = [[15] * 5 for _ in range(5)]
        # Two routes: BFS must choose four steps down over six steps up.
        self.open_path([
            (2, 2), (2, 3), (3, 3), (4, 3), (4, 2),
        ])
        self.open_path([
            (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2),
        ])
        self.player = Player(*self.maze.grid_to_pixel(4, 2), radius=4)
        self.manager = GhostsManager(
            Draw(pygame.Surface((100, 100))), self.maze, self.player,
        )
        self.manager.create_ghost(2, 2, 2, (2, 2), speed=3)
        self.ghost = self.manager.ghosts[0]

    def open_path(self, cells: list[tuple[int, int]]) -> None:
        opposite = {1: 4, 2: 8, 4: 1, 8: 2}
        for (x, y), (nx, ny) in zip(cells, cells[1:]):
            for direction, delta in DIRECTIONS.items():
                if delta == (nx - x, ny - y):
                    self.maze.maze[y][x] &= ~direction
                    self.maze.maze[ny][nx] &= ~opposite[direction]
                    break
            else:
                self.fail("Test paths must use adjacent cells")

    def test_bfs_follows_shortest_legal_route_around_walls(self) -> None:
        route = [(2, 3), (3, 3), (4, 3), (4, 2)]
        for expected in route:
            step = self.manager.choose_next_tile(self.ghost, (4, 2))
            self.assertIn(step, self.maze.get_available_moves(
                self.ghost.x, self.ghost.y,
            ))
            self.assertEqual(step, expected)
            self.ghost.x, self.ghost.y = expected
        self.assertIsNone(self.manager.choose_next_tile(self.ghost, (4, 2)))

    def test_bfs_stops_for_same_or_unreachable_target(self) -> None:
        for target in [(2, 2), (0, 0), (-1, 2), (5, 2)]:
            with self.subTest(target=target):
                self.assertIsNone(
                    self.manager.choose_next_tile(self.ghost, target),
                )

    def test_all_ghost_kinds_chase_player_with_bfs(self) -> None:
        for kind in ["blinky", "pinky", "inky", "clyde"]:
            with self.subTest(kind=kind):
                self.manager.ghosts.clear()
                self.manager.create_ghost(2, 2, 2, (0, 0), kind)
                ghost = self.manager.ghosts[0]
                self.manager.move_all()
                self.assertEqual((ghost.x, ghost.y), (2, 3))
                self.assertEqual(ghost.direction, 4)

    def test_movement_finishes_cell_before_turning_without_overshoot(
        self,
    ) -> None:
        start_x, start_y = self.maze.grid_to_pixel(2, 2)
        self.manager.move_all()
        for distance in [3, 6, 9, 10]:
            self.manager.update_all()
            self.assertEqual(self.ghost.pixel_x, start_x)
            self.assertEqual(self.ghost.pixel_y, start_y + distance)
            if distance < 10:
                self.manager.move_all()
                self.assertEqual((self.ghost.x, self.ghost.y), (2, 3))
        self.manager.move_all()
        self.assertEqual((self.ghost.x, self.ghost.y), (3, 3))
        self.manager.update_all()
        self.assertEqual(self.ghost.pixel_x, start_x + 3)
        self.assertEqual(self.ghost.pixel_y, start_y + 10)

    def test_chase_recalculates_for_player_at_next_cell_center(self) -> None:
        self.manager.move_all()
        self.manager.update_all()
        self.player.x, self.player.y = self.maze.grid_to_pixel(2, 0)
        self.manager.move_all()
        self.assertEqual((self.ghost.x, self.ghost.y), (2, 3))
        for _ in range(3):
            self.manager.update_all()
        self.manager.move_all()
        self.assertEqual((self.ghost.x, self.ghost.y), (2, 2))
        self.assertEqual(self.ghost.direction, 1)

    def test_frightened_ghost_does_not_double_back_in_corridor(self) -> None:
        self.ghost.x, self.ghost.y = (2, 3)
        self.ghost.direction = 4
        self.player.x, self.player.y = self.maze.grid_to_pixel(4, 3)
        self.assertEqual(
            self.manager.choose_frightened_tile(self.ghost), (3, 3),
        )

    def test_frightened_ghost_can_reverse_at_dead_end(self) -> None:
        self.open_path([(0, 4), (1, 4)])
        self.ghost.respawn()
        self.ghost.move(1, 4)
        self.ghost.pixel_x, self.ghost.pixel_y = (
            self.ghost.target_x, self.ghost.target_y,
        )
        self.ghost.direction = 2
        self.manager.frighten_all()
        self.manager.move_all()
        self.assertEqual((self.ghost.x, self.ghost.y), (0, 4))
        self.assertEqual(self.ghost.direction, 8)

    def test_blocked_ghost_has_no_frightened_move(self) -> None:
        self.ghost.x, self.ghost.y = (0, 0)
        self.assertIsNone(self.manager.choose_frightened_tile(self.ghost))

    def test_eaten_ghost_uses_bfs_to_spawn_and_respawns_on_timer(self) -> None:
        self.ghost.spawn = (4, 2)
        with patch("src.game.ghost.time.monotonic", return_value=100):
            self.ghost.get_eaten()
        with patch("src.game.ghost_manger.time.monotonic", return_value=101):
            self.manager.move_all()
        self.assertEqual(self.ghost.mode, "eaten")
        self.assertEqual((self.ghost.x, self.ghost.y), (2, 3))
        self.player.powered_up = True
        with patch("src.game.ghost_manger.time.monotonic", return_value=105):
            self.manager.move_all()
        self.assertEqual(self.ghost.mode, "frightened")
        self.assertEqual((self.ghost.x, self.ghost.y), (4, 2))
        self.assertTrue(self.ghost.is_at_target())

    def test_freeze_stops_route_choices_and_pixel_movement(self) -> None:
        self.manager.move_all()
        position = (self.ghost.pixel_x, self.ghost.pixel_y)
        target = (self.ghost.target_x, self.ghost.target_y)
        self.manager.frozen = True
        self.manager.move_all()
        self.manager.update_all()
        self.assertEqual((self.ghost.pixel_x, self.ghost.pixel_y), position)
        self.assertEqual((self.ghost.target_x, self.ghost.target_y), target)


if __name__ == "__main__":
    unittest.main()
