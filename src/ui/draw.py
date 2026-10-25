"""Small raster drawing helpers shared by game screens."""

import pygame

from ..resources import resource_path

Color = tuple[int, int, int]


class Draw:
    """Draw text, images and primitives onto a surface."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Keep a target surface and cache fonts.

        Args:
            screen: Surface used to display or draw the game.

        Returns:
            None.
        """
        self.screen = screen
        self.fonts: dict[int, pygame.font.Font] = {}
        pygame.font.init()

    def draw_horizontal_line(
        self,
        start_x: int,
        y: int,
        end_x: int,
        color: Color,
        thickness: int = 1,
    ) -> None:
        """Fill a horizontal strip.

        Args:
            start_x: First horizontal pixel coordinate, inclusive.
            y: Vertical canvas coordinate in pixels.
            end_x: Final horizontal pixel coordinate, exclusive.
            color: RGB color used for the text, line or border.
            thickness: Stroke thickness in pixels.

        Returns:
            None.
        """
        self.screen.fill(color, (start_x, y, end_x - start_x, thickness))

    def draw_vertical_line(
        self,
        x: int,
        start_y: int,
        end_y: int,
        color: Color,
        thickness: int = 1,
    ) -> None:
        """Fill a vertical strip.

        Args:
            x: Horizontal canvas coordinate in pixels.
            start_y: First vertical pixel coordinate, inclusive.
            end_y: Final vertical pixel coordinate, exclusive.
            color: RGB color used for the text, line or border.
            thickness: Stroke thickness in pixels.

        Returns:
            None.
        """
        self.screen.fill(color, (x, start_y, thickness, end_y - start_y))

    def load_image(self, path: str) -> pygame.Surface:
        """Load a bundled image independently of the working directory.

        Args:
            path: Project-relative resource filename.

        Returns:
            pygame.Surface: The loaded image converted to the display alpha
                format.

        Raises:
            OSError: The image file cannot be read.
            pygame.error: The image format cannot be decoded.
        """
        return pygame.image.load(str(resource_path(path))).convert_alpha()

    def _wall(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        thickness: int,
    ) -> None:
        """Draw a rounded wall with a restrained blue inner edge.

        Args:
            start: First endpoint of the wall segment in pixels.
            end: Last endpoint of the wall segment in pixels.
            thickness: Stroke thickness in pixels.

        Returns:
            None.
        """
        for width, color in (
            (thickness, (32, 58, 87)),
            (max(1, thickness // 2), (99, 163, 225)),
        ):
            radius = width // 2
            if start[1] == end[1]:
                self.draw_horizontal_line(
                    start[0],
                    start[1] - radius,
                    end[0] + 1,
                    color,
                    width,
                )
            else:
                self.draw_vertical_line(
                    start[0] - radius,
                    start[1],
                    end[1] + 1,
                    color,
                    width,
                )
            self.draw_circle(*start, radius, color)
            self.draw_circle(*end, radius, color)

    def draw_maze(
        self,
        cell_x: int,
        cell_y: int,
        cell: int,
        cell_size: int,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> None:
        """Draw crisp wall geometry without stretching bitmap tiles.

        Args:
            cell_x: Column of the maze cell to draw.
            cell_y: Row of the maze cell to draw.
            cell: North/east/south/west wall-bit mask of the maze cell.
            cell_size: Side length of one maze tile in pixels.
            offset_x: Horizontal position of the maze origin in pixels.
            offset_y: Vertical position of the maze origin in pixels.

        Returns:
            None.
        """
        x = cell_x * cell_size + offset_x
        y = cell_y * cell_size + offset_y
        thickness = max(3, cell_size // 12)
        inset = thickness // 2
        left, top = x + inset, y + inset
        right, bottom = x + cell_size - inset - 1, y + cell_size - inset - 1
        for bit, start, end in (
            (1, (left, top), (right, top)),
            (2, (right, top), (right, bottom)),
            (4, (left, bottom), (right, bottom)),
            (8, (left, top), (left, bottom)),
        ):
            if cell & bit:
                self._wall(start, end, thickness)

    def draw_circle(
        self,
        center_x: int,
        center_y: int,
        radius: int,
        color: Color,
    ) -> None:
        """Fill a circle using horizontal pixel spans.

        Args:
            center_x: Horizontal center of the circle in pixels.
            center_y: Vertical center of the circle in pixels.
            radius: Radius in pixels for drawing or collision detection.
            color: RGB color used for the text, line or border.

        Returns:
            None.
        """
        for dy in range(-radius, radius + 1):
            half = int((radius * radius - dy * dy) ** 0.5)
            self.draw_horizontal_line(
                center_x - half, center_y + dy, center_x + half + 1, color
            )

    def measure_text(self, text: str, size: int) -> tuple[int, int]:
        """Measure text with the same cached font used for rendering.

        Args:
            text: Text to measure, render or process.
            size: Requested font size in pixels.

        Returns:
            tuple[int, int]: Width and height of the rendered text in pixels.
        """
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size].size(text)

    def fit_text(self, text: str, size: int, max_width: int) -> int:
        """Choose a font size that fits a score or label inside its column.

        Args:
            text: Text to measure, render or process.
            size: Requested font size in pixels.
            max_width: Maximum text width in pixels; None disables fitting.

        Returns:
            int: A positive font size that fits, down to the minimum size of
                one.
        """
        width = self.measure_text(text, size)[0]
        if width > max_width:
            size = max(1, size * max_width // width)
            while size > 1 and self.measure_text(text, size)[0] > max_width:
                size -= 1
        return size

    def draw_text(
        self,
        text: str,
        x: int,
        y: int,
        size: int,
        color: Color,
        centre: bool = False,
        max_width: int | None = None,
    ) -> None:
        """Render text, optionally centered and fitted to available width.

        Args:
            text: Text to measure, render or process.
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.
            size: Requested font size in pixels.
            color: RGB color used for the text, line or border.
            centre: Whether x is the horizontal center rather than the left
                edge.
            max_width: Maximum text width in pixels; None disables fitting.

        Returns:
            None.
        """
        if max_width is not None:
            size = self.fit_text(text, size, max_width)
        self.measure_text(text, size)
        surface = self.fonts[size].render(text, True, color)
        if centre:
            x -= surface.get_width() // 2
        self.screen.blit(surface, (x, y))

    def clear(self, color: Color = (7, 11, 24)) -> None:
        """Fill the target with one color.

        Args:
            color: RGB color used for the text, line or border.

        Returns:
            None.
        """
        self.screen.fill(color)

    def draw_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Color,
        thickness: int = 1,
    ) -> None:
        """Draw the four edges of a rectangle.

        Args:
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.
            color: RGB color used for the text, line or border.
            thickness: Stroke thickness in pixels.

        Returns:
            None.
        """
        self.draw_horizontal_line(x, y, x + width, color, thickness)
        self.draw_horizontal_line(x, y + height, x + width, color, thickness)
        self.draw_vertical_line(x, y, y + height, color, thickness)
        self.draw_vertical_line(x + width, y, y + height, color, thickness)

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        """Copy a prepared image onto the target.

        Args:
            image: Prepared image surface to copy onto the target.
            x: Horizontal canvas coordinate in pixels.
            y: Vertical canvas coordinate in pixels.

        Returns:
            None.
        """
        self.screen.blit(image, (x, y))
