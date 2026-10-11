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

    def move_selection(self, direction: int) -> None:
        self.selected = (self.selected + direction) % len(self.options)

    def select(self) -> str:
        return self.options[self.selected]

    def draw_menu(self):
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
            text = f"▶  {op}" if i == self.selected else f"  {op}"
            self.draw.draw_text(
                text, self.width // 2, menu_start_y, self.options_size, color, True
            )
            menu_start_y += self.spacing


import pygame

pygame.init()
screen = pygame.display.set_mode()
clock = pygame.time.Clock()
draw = Draw(screen, 20)

menu = Menu(draw)
rununing = True
while rununing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rununing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu.move_selection(-1)
            elif event.key == pygame.K_DOWN:
                menu.move_selection(1)

            elif event.key == pygame.K_RETURN:
                action = menu.select()
                print(action)

    screen.fill((5, 8, 20))
    menu.draw_menu()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
