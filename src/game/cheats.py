"""Provide keyboard shortcuts for gameplay evaluation."""

from .player import Player
from .game import Game
from .ghost_manger import GhostsManager
import pygame


class Cheats:
    """Provide evaluation shortcuts."""

    def __init__(
        self, player: Player, game: Game, ghosts: GhostsManager
    ) -> None:
        """Initialize this object and its dependencies.

        Args:
            player: Player whose position, lives or power state is used.
            game: Active game state, score and timing information.
            ghosts: Manager of the active ghosts.

        Returns:
            None.
        """
        self.player = player
        self.game = game

        self.ghosts = ghosts

    def handle_key(self, key: int) -> bool:
        """Apply a cheat key and report whether to skip the level.

        Args:
            key: Pygame key code to interpret as a cheat.

        Returns:
            bool: True when this key requests an immediate level skip.
        """
        if key == pygame.K_i:
            self.player.toggle_invincibility()

        elif key == pygame.K_s:
            return True

        elif key == pygame.K_f:
            self.ghosts.frozen = not self.ghosts.frozen

        elif key == pygame.K_l:
            self.player.add_life()

        return False
