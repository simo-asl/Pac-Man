from .player import Player
from .game import Game
import pygame


class Cheats:

    def __init__(self, player: Player, game: Game) -> None:
        self.player = player
        self.game = game

    def handle_key(self, key: int) -> None:
        if key == pygame.K_i:
            self.player.toggle_invincibility()
        elif key == pygame.K_s:
            self.game.next_level()
        # Key F for freeze the ghosts
        # Pass for Now bcuz we don't have the ghosts implementation
        elif key == pygame.K_f:
            pass
        # We can add more cheats later
