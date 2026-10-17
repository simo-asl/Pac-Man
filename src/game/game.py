from .player import Player
from .pacgum import Pacgum, SuperPacgum
from .ghost_manger import GhostsManager
import pygame

from ..parsing import GameConfig


class Game:
    def __init__(
        self,
        screen: pygame.Surface,
        s_width: int = 900,
        s_height: int = 900,
        config: GameConfig | None = None,
    ) -> None:

        self.config = config if config is not None else GameConfig()
        self.level_start_time = pygame.time.get_ticks()
        self.score: int = 0
        self.s_height: int = s_height
        self.s_width: int = s_width
        self.level: int = 1
        self.screen: pygame.Surface = screen
        self.death_time = 0
        self.paused = False

    def add_score(self, add: int) -> None:

        self.score += add

    def level_complete(
        self, pacgums: list[Pacgum], super_pacgums: list[SuperPacgum]
    ) -> bool:

        for i in pacgums:
            if not i.eaten:
                return False
        for i in super_pacgums:
            if not i.eaten:
                return False
        return True

    def next_level(self) -> None:
        self.level += 1
        self.level_start_time = pygame.time.get_ticks()

    def level_time_remaining(self) -> int:
        elapsed = (pygame.time.get_ticks() - self.level_start_time) // 1000
        return max(0, self.config.level_max_time - elapsed)

    def create_pacgums(
        self, pos: list[tuple[int, int]], count: int | None = None
    ) -> list[Pacgum]:

        pacgums = []
        requested = self.config.pacgum if count is None else count
        count_to_place = min(max(0, requested), len(pos))
        # Spread dots across the maze rather than filling its first cells.
        selected = [pos[i * len(pos) // count_to_place]
                    for i in range(count_to_place)] if count_to_place else []
        for x, y in selected:
            pacgums.append(Pacgum(x, y, 3, self.config.points_per_pacgum))
        return pacgums

    def create_super_pacgums(self, pos: list[tuple[int, int]]) -> list[SuperPacgum]:

        super_pacgums: list[SuperPacgum] = []

        for x, y in pos:
            super_pacgums.append(SuperPacgum(x, y, self.config.points_per_super_pacgum))

        return super_pacgums

    def collision(self, player: Player, pacgum: Pacgum) -> None:
        dx = player.x - pacgum.x
        dy = player.y - pacgum.y

        collision_radius = player.radius + pacgum.radius

        if dx * dx + dy * dy <= collision_radius ** 2:
            if not pacgum.eaten:
                pacgum.get_eaten()
                self.add_score(pacgum.points)

                if isinstance(pacgum, SuperPacgum):
                    player.activate_power()

    def check_all_collisions(self, player: Player, superpacgums: list[SuperPacgum],
                             pacgums: list[Pacgum], ghosts: GhostsManager) -> None:
        
        if self.paused or not player.alive:
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
        if self.paused:
            return
        self.paused = True
        self.death_time = pygame.time.get_ticks()

    def update_death(self, player: Player, ghosts: GhostsManager) -> None:
        if not self.paused:
            return

        now = pygame.time.get_ticks()
        if now - self.death_time >= 1000:
            self.reset_positions(player, ghosts)
            self.paused = False

    def reset_positions(self, player: Player, ghosts: GhostsManager):
        
        player.x, player.y = player.respawn
        player.target_x, player.target_y = player.respawn
        for ghost in ghosts.ghosts:
            ghost.respawn()
        player.powered_up = False

        

