import pygame

# Kan7awel nreproduci ga3 pygame li gha nhtajo cause all of them forbiden


class Draw:
    def __init__(self, screen: pygame.Surface, cell_size: int = 20):
        self.CELL_SIZE = cell_size
        self.screen: pygame.Surface = screen

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int, color, thickness: int = 1
    ) -> None:
        for offset in range(thickness):
            for x in range(start_x, end_x):
                self.screen.set_at((x, y + offset), color)

    def draw_vertical_line(
        self, x: int, start_y: int, end_y: int, color, thickness: int = 1
    ) -> None:
        for offset in range(thickness):
            for y in range(start_y, end_y):
                self.screen.set_at((x + offset, y), color)

    def draw_maze(self, cell_x, cell_y, cell, color, thickness=1) -> None:
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

    def draw_circle(self, center_x: int, center_y: int, radius: int, color) -> None:
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                dx = x - center_x
                dy = y - center_y
                if dx * dx + dy * dy <= radius * radius:
                    self.screen.set_at((x, y), color)

    def draw_text(self, text: str, x: int, y: int, size: int, color) -> None:
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def clear(self, color=(0, 0, 0)) -> None:
        self.screen.fill(color)

    def draw_rect(self, x, y, width, height, color, thickness=1) -> None:
        self.draw_vertical_line(x, y, y + height, color, thickness)
        self.draw_horizontal_line(x, y, x + width, color, thickness)
        self.draw_horizontal_line(x, y + height, x + width, color, thickness)
        self.draw_vertical_line(x + width, y, y + height, color, thickness)

    def load_image(self, path: str) -> pygame.Surface:
        return pygame.image.load(path)

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        self.screen.blit(image, (x, y))
