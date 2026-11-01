"""Provide keyboard shortcuts for evaluation."""

from .player import Player
from .game import Game
from .ghost_manger import GhostsManager
import pygame


class Cheats:

    """Expose evaluation shortcuts for the current game and actors.
    """
    def __init__(
        self, player: Player, game: Game, ghosts: GhostsManager
    ) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            player: Player whose lives, position or power state is used.
            game: Current game controller or gameplay state.
            ghosts: Manager holding the ghosts affected by this operation.

        Returns:
            None.
        """
        self.player = player
        self.game = game

        self.ghosts = ghosts

    def handle_key(self, key: int) -> bool:
        """Apply an evaluation cheat and indicate whether to skip a level.

        Args:
            key: Pygame key code identifying the requested cheat.

        Returns:
            True only when the level-skip cheat was requested.
        """
        if key == pygame.K_i:
            self.player.toggle_invincibility()

        elif key == pygame.K_s:
            return True

        elif key == pygame.K_f:
            self.ghosts.frozen = not self.ghosts.frozen

        elif key == pygame.K_l:
            self.player.add_life()

        elif key == pygame.K_b:
            # Refresh the normal power-pellet effect.
            self.player.activate_power()

        elif key == pygame.K_t:
            # Move the deadline forward without disrupting pause accounting.
            self.game.level_start_time += 30_000

        elif key == pygame.K_m:
            self.game.add_score(1_000)

        elif key == pygame.K_r:
            # Return actors to their starting positions without losing a life.
            self.game.reset_positions(self.player, self.ghosts)

        return False
