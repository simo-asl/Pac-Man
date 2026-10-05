import pygame


class Draw:
    def __init__(self, screen, cell_size: int = 20):
        self.CELL_SIZE = cell_size
        self.screen = screen

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int, color, thickness=1
    ):
        for offset in range(thickness):
            for x in range(start_x, end_x):
                self.screen.set_at((x, y + offset), color)

    def draw_vertical_line(self, x: int, start_y: int, end_y: int, color, thickness=1):
        for offset in range(thickness):
            for y in range(start_y, end_y):
                self.screen.set_at((x + offset, y), color)

    def draw_maze(self, cell_x, cell_y, cell, color, thickness=1):
        x = cell_x * self.CELL_SIZE
        y = cell_y * self.CELL_SIZE
        x2 = x + self.CELL_SIZE
        y2 = y + self.CELL_SIZE

        if cell & 1:
            self.draw_horizontal_line(x, y, x2, color, thickness)
        if cell & 2:
            self.draw_vertical_line(x2, y, y2, color, thickness)
        if cell & 4:
            self.draw_horizontal_line(x, y2, x2, color, thickness)
        if cell & 8:
            self.draw_vertical_line(x, y, y2, color, thickness)

    def draw_circle(self, center_x: int, center_y: int, radius: int, color):
        for y in range(center_y - radius, center_y + radius - 1):
            for x in range(center_x - radius, center_x + radius - 1):
                dx = x - center_x
                dy = y - center_y
                if dx * dx + dy * dy <= radius * radius:
                    self.screen.set_at((x, y), color)

    def draw_text(self, text: str, x: int, y: int, size: int, color):
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def clear(self, color=(0, 0, 0)) -> None:
        self.screen.fill(color)
