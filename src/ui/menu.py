import pygame

from ..game import score
from ..maze import Maze
from .draw import Draw


class Menu:
    def __init__(self, draw: Draw):
        self.draw = draw
        self.selected = 0
        self.height = self.draw.screen.get_height()
        self.title_size = max(36, self.height // 9)
        self.options_size = max(20, self.height // 20)
        self.spacing = max(35, self.height // 14)
        self.width = self.draw.screen.get_width()
        self.options = [
            "START GAME",
            "HIGHSCORES",
            "INSTRUCTIONS",
            "EXIT",
        ]
        self.t = self.draw.load_image("src/game/assets/backgrounds/main_menu.png")

        self.resu = pygame.transform.scale(self.t, (self.width, self.height))

    def move_selection(self, direction: int) -> None:
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected]

    def one_draw_maze(
        self, maze: Maze, thinkeess: int = 5, offset_x: int = 0, offset_y: int = 0
    ):
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(
                    x,
                    y,
                    cell,
                    (255, 220, 50),
                    maze.CELL_SIZE,
                    thinkeess,
                    offset_x,
                    offset_y,
                )

    def draw_menu(self):
        self.draw.screen.fill((0, 0, 0))
        self.draw.draw_image(self.resu, 0, 0)
        title_y = self.height // 8
        self.draw.draw_text(
            "PAC-MAN", self.width // 2, title_y, self.title_size, (255, 220, 50), True
        )
        menu_start_y = self.height // 3 - 50
        box_width = self.width // 3
        box_height = min(self.spacing - 8, self.options_size + 20)
        box_x = (self.width - box_width) // 2
        for i, op in enumerate(self.options):
            color = (255, 220, 50) if i == self.selected else (220, 220, 220)
            self.draw.draw_rect(
                box_x,
                menu_start_y - 25,
                box_width,
                box_height,
                color,
                10,
            )
            text = f"▶ {op}" if i == self.selected else f"  {op}"
            self.draw.draw_text(
                text, self.width // 2, menu_start_y, self.options_size, color, True
            )
            menu_start_y += self.spacing

    def draw_highscore(self, scores: list[score]) -> None:
        self.draw.screen.fill((0, 0, 0))
        high_h = 150
        self.draw.draw_text(
            "HighScore",
            (self.width // 2),
            int(self.height * 0.05),
            90,
            (155, 255, 252),
            centre=True,
        )
        t = 0
        space = (self.height * 0.07) + self.height // 9
        for i, s in enumerate(scores):
            self.draw.draw_text(
                f"{i + 1}--{s.name}:",
                (self.width // 2) - 50,
                (250) + t,
                43,
                (244, 244, 244),
                True,
            )
            self.draw.draw_text(
                str(s.score),
                (self.width // 2) + 50,
                (250) + t,
                43,
                (244, 244, 244),
                True,
            )
            t += 50


t = []
a = 50
for i in range(10):
    t.append(score(name="tar", score=193 + a))
    a += 50


pygame.init()
a = pygame.display.set_mode((1200, 1800))

d = Draw(a)
menu = Menu(d)
while True:
    menu.draw_highscore(t)
    pygame.display.flip()
