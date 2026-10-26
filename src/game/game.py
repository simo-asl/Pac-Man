"""Manage scoring, collisions, level timing and pauses."""

from .player import Player
from .pacgum import Pacgum, SuperPacgum
from .ghost_manger import GhostsManager
import pygame
import random

from ..parsing import GameConfig


class Game:
    """Manage score, pellet collisions, pauses and level deadlines.
    """
    def __init__(
        self,
        config: GameConfig | None = None,
    ) -> None:

        """Initialize this object and its runtime dependencies.

        Args:
            config: Validated game configuration; None uses default
                settings.

        Returns:
            None.
        """
        self.config = config if config is not None else GameConfig()
        self.level_start_time = pygame.time.get_ticks()
        self.total_pause_time = 0
        self.score: int = 0
        self.death_time = 0
        self.paused = False
        self.manual_pause = False
        self.manual_pause_start = 0

    def add_score(self, add: int) -> None:

        """Increase the current score by the supplied point amount.

        Args:
            add: Nonnegative point amount to add to the current score.

        Returns:
            None.
        """
        self.score += add

    def level_complete(
        self, pacgums: list[Pacgum], super_pacgums: list[SuperPacgum]
    ) -> bool:

        """Check whether every normal and power pellet was eaten.

        Args:
            pacgums: Normal pellets belonging to the current level.
            super_pacgums: Power pellets belonging to the current level.

        Returns:
            True if every normal and power pellet is eaten.
        """
        for i in pacgums:
            if not i.eaten:
                return False
        for i in super_pacgums:
            if not i.eaten:
                return False
        return True

    def next_level(self) -> None:
        """Advance progression while retaining score and remaining lives.

        Returns:
            None.
        """
        self.level_start_time = pygame.time.get_ticks()
        self.total_pause_time = 0
        self.paused = False
        self.manual_pause = False
        self.death_time = 0
        self.manual_pause_start = 0

    def level_time_remaining(self) -> int:

        """Calculate remaining seconds excluding game pauses.

        Returns:
            Nonnegative number of seconds left for the level.
        """
        now = pygame.time.get_ticks()

        if self.manual_pause:
            now = self.manual_pause_start
        elif self.paused:
            now = self.death_time

        elapsed = now - self.level_start_time - self.total_pause_time

        remaining = self.config.level_max_time - elapsed // 1000

        return max(0, remaining)

    def create_pacgums(
        self,
        positions: list[tuple[int, int]],
        cell_size: int
    ) -> list[Pacgum]:

        """Place normal pellets in at least seventy percent of corridors.

        Args:
            positions: Available corridor pixel centers for normal pellets.

        Returns:
            Normal pellets created at sampled corridor positions.
        """
        pacgums = []

        minimum = len(positions) * 70 // 100
        count = max(minimum, min(self.config.pacgum, len(positions)))

        selected = random.sample(positions, count)

        radius = max(2, round(cell_size * 0.10))
        for x, y in selected:
            pacgum = Pacgum(
                x,
                y,
                radius,
                self.config.points_per_pacgum,
            )
            pacgums.append(pacgum)

        return pacgums

    def create_superpac(self,
        pos: list[tuple[int, int]],
        cell_size: int
        ) -> list[SuperPacgum]:

        """Create power pellets at the supplied corner positions.

        Args:
            pos: Corner pixel centers for the power pellets.

        Returns:
            Power pellets created at the supplied positions.
        """
        super_pacgums: list[SuperPacgum] = []

        radius = max(2, round(cell_size * 0.18))
        for x, y in pos:
            super_pacgums.append(
                SuperPacgum(x, y, radius, self.config.points_per_super_pacgum))

        return super_pacgums

    def collision(self, player: Player, pacgum: Pacgum) -> None:
        """Consume a touched pellet and apply its score and power effect.

        Args:
            player: Player whose lives, position or power state is used.
            pacgum: Normal or power pellet to test against the player.

        Returns:
            None.
        """
        dx = player.x - pacgum.x
        dy = player.y - pacgum.y

        collision_radius = player.radius + pacgum.radius

        if dx * dx + dy * dy <= collision_radius ** 2:
            if not pacgum.eaten:
                pacgum.get_eaten()
                self.add_score(pacgum.points)

                if isinstance(pacgum, SuperPacgum):
                    player.activate_power()

    def check_all_collisions(self, player: Player,
                             superpacgums: list[SuperPacgum],
                             pacgums: list[Pacgum],
                             ghosts: GhostsManager) -> None:

        """Resolve pellet and ghost contacts for the active player.

        Args:
            player: Player whose lives, position or power state is used.
            superpacgums: Power pellets belonging to the current level.
            pacgums: Normal pellets belonging to the current level.
            ghosts: Manager holding the ghosts affected by this operation.

        Returns:
            None.
        """
        if self.paused or self.manual_pause or not player.alive:
            return

        for pacgum in pacgums:
            self.collision(player, pacgum)

        for superpac in superpacgums:
            self.collision(player, superpac)

        for ghost in ghosts.ghosts:
            if not ghosts.is_collesion(ghost):
                continue

            if ghost.mode == "frightened":
                ghost.get_eaten()
                self.add_score(self.config.points_per_ghost)
            elif ghost.mode == "chase" and not player.invincible:
                player.lose_life()
                if player.alive:
                    self.start_death()
                break

    def start_death(self) -> None:
        """Start the temporary pause before respawning surviving actors.

        Returns:
            None.
        """
        if self.paused:
            return
        self.paused = True
        self.death_time = pygame.time.get_ticks()

    def toggle_pause(
        self, player: Player, ghosts: GhostsManager
    ) -> None:
        """Pause or resume while preserving gameplay timers.

        Args:
            player: Player whose power timer must stop during pause.
            ghosts: Ghosts whose respawn timers must stop during pause.

        Returns:
            None.
        """
        if self.paused:
            return
        now = pygame.time.get_ticks()

        if self.manual_pause:
            duration = now - self.manual_pause_start
            self.total_pause_time += duration
            if player.powered_up:
                player.power_start_time += duration
            for ghost in ghosts.ghosts:
                if ghost.mode == "eaten":
                    ghost.time_eaten += duration / 1000
            self.manual_pause = False
        else:
            self.manual_pause = True
            self.manual_pause_start = now

    def update_death(self, player: Player, ghosts: GhostsManager) -> None:

        """Respawn actors when the temporary death pause expires.

        Args:
            player: Player whose lives, position or power state is used.
            ghosts: Manager holding the ghosts affected by this operation.

        Returns:
            None.
        """
        if not self.paused:
            return

        now = pygame.time.get_ticks()

        if now - self.death_time >= 1000:

            pause_duration = now - self.death_time

            self.total_pause_time += pause_duration

            self.reset_positions(player, ghosts)

            self.paused = False

    def reset_positions(self, player: Player, ghosts: GhostsManager) -> None:

        """Restore player and ghost spawn positions and clear power.

        Args:
            player: Player whose lives, position or power state is used.
            ghosts: Manager holding the ghosts affected by this operation.

        Returns:
            None.
        """
        player.x, player.y = player.respawn
        player.target_x, player.target_y = player.respawn
        for ghost in ghosts.ghosts:
            ghost.respawn()
        player.powered_up = False
