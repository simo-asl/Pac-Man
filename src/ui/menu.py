import pygame

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
        self.maze_created = [False for _ in range(10)]
        self.cache = {}

    def move_selection(self, direction: int) -> None:
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected]

    def one_draw_maze(
        self, maze: Maze, thinkeess: int = 5, offset_x: int = 0, offest_y: int = 0
    ):
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                self.draw.draw_maze(
                    x + offset_x,
                    y + offest_y,
                    cell,
                    (255, 220, 50),
                    maze.CELL_SIZE,
                    thinkeess,
                )

    def menu_game(self, maze: Maze, thinkeess: int = 5, level: int = 0):
        t = pygame.Surface((self.width, self.height))
        if not self.maze_created[level]:
            self.one_draw_maze(maze, thinkeess)
            self.maze_created[level] = True
            t.blit(self.draw.screen, (0, 0))
            self.cache[level] = t
        else:
            self.draw.draw_image(self.cache[level], 0, 0)
        self.draw.draw_text(
            f">> Level {level} <<", (self.width // 5) * 4 - 230, 10, 80, (255, 220, 50)
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


# import pygame
#
# pygame.init()
# screen_width = 1500
# screen_height = 1200
# screen = pygame.display.set_mode([screen_width, screen_height])
# clock = pygame.time.Clock()
# draw = Draw(screen)
# from ..parsing import Parser
#
# pa = Parser("config.json")
# maze = Maze(pa.parser(), draw, 0, (screen_width, screen_height))
# pygame.display.set_caption("Pac-Man")
# menu = Menu(draw)
# rununing = True
#
#
# action = None
# while rununing:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             rununing = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 menu.move_selection(-1)
#             elif event.key == pygame.K_DOWN:
#                 menu.move_selection(1)
#             elif event.key == pygame.K_RETURN:
#                 action = menu.select()
#         if action is None:
#             menu.draw_menu()
#         if action:
#             match action:
#                 case "START GAME":
#                     screen.fill((0, 0, 0))
#                     menu.one_draw_maze(maze)
#                 case _:
#                     action = None
#
#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()
