from .player import Player
from .game import Game
from .ghost_manger import GhostsManager
import pygame


class Cheats:

    def __init__(self, player: Player, game: Game, ghosts: GhostsManager) -> None:
        self.player = player
        self.game = game

        self.ghosts = ghosts

    def handle_key(self, key: int) -> bool:
        if key == pygame.K_i:
            self.player.toggle_invincibility()

        elif key == pygame.K_s:
            return True

        elif key == pygame.K_f:
            self.ghosts.frozen = not self.ghosts.frozen

        elif key == pygame.K_l:
            self.player.add_life()

        return False
