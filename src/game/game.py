from .player import Player
from .pacgum import Pacgum, SuperPacgum
import pygame


# I tried to keep everything simple and readable
# If you find any bug or misunderstanding, just reach out to me
# Maybe I cooked, maybe I didn't hhhhhhh
class Game:

    def __init__(self, screen: pygame.Surface,
                 s_width: int = 900, s_height: int = 900):

        self.score: int = 0
        self.s_height: int = s_height
        self.s_width: int = s_width
        self.level: int = 1
        self.screen: pygame.Surface = screen

    def add_score(self, add: int) -> None:

        self.score += add

    def level_complete(self, pacgums: list[Pacgum],
                       super_pacgums: list[SuperPacgum]) -> bool:

        for i in pacgums:
            if not i.eaten:
                return False
        for i in super_pacgums:
            if not i.eaten:
                return False
        return True

    def next_level(self) -> None:
        self.level += 1

    def create_pacgums(self, pos: list[tuple[int, int]]) -> list[Pacgum]:

        pacgums = []
        for x, y in pos:
            pacgums.append(Pacgum(x, y, 3))
        return pacgums

    def create_super_pacgums(self,
                             pos: list[tuple[int, int]]) -> list[SuperPacgum]:

        super_pacgums: list[SuperPacgum] = []

        for x, y in pos:
            super_pacgums.append(SuperPacgum(x, y))

        return super_pacgums

    # collision temp cuz mlx mafihach collision detection mais pygame fiha so
    # i'll find fix it later
    # beta version of collisionnnnnnnnnn
    def collision(self, player: Player, pacgum: Pacgum) -> None:

        player_rect = pygame.Rect(
            player.x - player.radius,
            player.y - player.radius,
            player.radius * 2,
            player.radius * 2
        )

        pacgum_rect = pygame.Rect(
            pacgum.x - pacgum.radius,
            pacgum.y - pacgum.radius,
            pacgum.radius * 2,
            pacgum.radius * 2
        )

        if not pacgum.eaten and player_rect.colliderect(pacgum_rect):
            pacgum.get_eaten()
            self.add_score(pacgum.points)
            if isinstance(pacgum, SuperPacgum):
                player.activate_power()
