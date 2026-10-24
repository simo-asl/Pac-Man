import pygame

# Kan7awel nreproduci ga3 pygame li gha nhtajo cause all of them forbiden


class Draw:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.walls = None
        pygame.font.init()

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int, color, thickness: int = 1
    ) -> None:
        for offset in range(thickness):
            for x in range(start_x, end_x):
                if not (
                    0 <= x < self.screen.get_width()
                    and 0 <= y + offset < self.screen.get_height()
                ):
                    continue
                self.screen.set_at((x, y + offset), color)

    def draw_vertical_line(
        self, x: int, start_y: int, end_y: int, color, thickness: int = 1
    ) -> None:
        for offset in range(thickness):
            for y in range(start_y, end_y):
                if not (
                    0 <= x + offset < self.screen.get_width()
                    and 0 <= y < self.screen.get_height()
                ):
                    continue
                self.screen.set_at((x + offset, y), color)

    def load_image(self, path: str) -> pygame.Surface:
        return pygame.image.load(path)

    def load_walls(self, cell_size: int):
        walls = {}
        for i in range(16):
            wall = self.load_image(f"src/game/assets/maze/{i}.png")
            walls[i] = pygame.transform.scale(wall, (cell_size, cell_size))

        return walls

    def draw_maze(
        self,
        cell_x: int,
        cell_y: int,
        cell: int,
        cell_size: int,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> None:
        if not self.walls:
            self.walls = self.load_walls(cell_size)
        x = cell_x * cell_size + offset_x
        y = cell_y * cell_size + offset_y

        self.draw_image(self.walls[cell], x, y)

    def draw_circle(
        self,
        center_x: int,
        center_y: int,
        radius: int,
        color: tuple[int, int, int],
    ) -> None:
        width, height = self.screen.get_size()

        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                if not (0 <= x < width and 0 <= y < height):
                    continue

                dx = x - center_x
                dy = y - center_y

                if dx * dx + dy * dy <= radius * radius:
                    self.screen.set_at((x, y), color)

    def draw_text(
        self, text: str, x: int, y: int, size: int, color, centre: bool = False
    ) -> None:
        font = pygame.font.Font(None, size=size)
        surface = font.render(text, True, color)
        if centre:
            x -= surface.get_width() // 2
        self.screen.blit(surface, (x, y))

    def clear(self, color=(0, 0, 0)) -> None:
        self.screen.fill(color)

    def draw_rect(self, x, y, width, height, color, thickness=1) -> None:
        self.draw_vertical_line(x, y, y + height, color, thickness)
        self.draw_horizontal_line(x, y, x + width, color, thickness)
        self.draw_horizontal_line(x, y + height, x + width, color, thickness)
        self.draw_vertical_line(x + width, y, y + height, color, thickness)

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        self.screen.blit(image, (x, y))
