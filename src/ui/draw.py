"""Render the interface using MLX-style image and pixel operations."""

import sys
from math import isqrt
from typing import cast

from bdfparser import Font

import pygame

from ..resources import resource_path

Color = tuple[int, int, int]


class Draw:
    """Draw images, text masks and pixel primitives on one target.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            screen: Surface used as the drawing target or game window.

        Returns:
            None.
        """
        self.screen: pygame.Surface = screen
        self.walls: dict[int, dict[int, pygame.Surface]] = {}
        self.font = Font(str(resource_path('assets/fonts/Tamzen10x20b.bdf')))
        self.glyph_pixels: dict[str, list[list[int]]] = {}
        self.text_images: dict[
            tuple[str, int, Color], pygame.Surface
        ] = {}

    def draw_horizontal_line(
        self, start_x: int, y: int, end_x: int,
        color: Color, thickness: int = 1
    ) -> None:
        """Write a horizontal strip of clipped pixels.

        Args:
            start_x: First horizontal pixel coordinate, inclusive.
            y: Vertical position in pixels.
            end_x: Last horizontal pixel coordinate, exclusive.
            color: RGB color for the pixels, outline or text.
            thickness: Stroke width in pixels.

        Returns:
            None.
        """
        self.fill_rect(start_x, y, end_x - start_x, thickness, color)

    def draw_vertical_line(
        self, x: int, start_y: int, end_y: int,
        color: Color, thickness: int = 1
    ) -> None:
        """Write a vertical strip of clipped pixels.

        Args:
            x: Horizontal position in pixels.
            start_y: First vertical pixel coordinate, inclusive.
            end_y: Last vertical pixel coordinate, exclusive.
            color: RGB color for the pixels, outline or text.
            thickness: Stroke width in pixels.

        Returns:
            None.
        """
        self.fill_rect(x, start_y, thickness, end_y - start_y, color)

    def load_image(
        self, path: str, size: tuple[int, int] | None = None
    ) -> pygame.Surface:
        """Load a bundled PNG independently of the working directory.

        Args:
            path: Project-relative resource filename.
            size: Optional target width and height in pixels.

        Returns:
            Decoded PNG surface ready for image placement.

        Raises:
            OSError: The image file cannot be opened.
            pygame.error: The image cannot be decoded.
        """
        image = pygame.image.load(str(resource_path(path)))
        return self.scale_image(image, size) if size is not None else image

    def load_walls(self, cell_size: int) -> dict[int, pygame.Surface]:
        """Prepare all wall-mask images at the requested cell size.

        Args:
            cell_size: Width and height of one maze cell in pixels.

        Returns:
            Mapping from wall masks zero through fifteen to sized tile
            images.
        """
        walls = {}
        for i in range(16):
            walls[i] = self.load_image(
                f"src/game/assets/maze/{i}.png", (cell_size, cell_size),
            )

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
        """Place the image matching a cell wall mask on the maze grid.

        Args:
            cell_x: Column of the maze cell to render.
            cell_y: Row of the maze cell to render.
            cell: North/east/south/west wall mask identifying the tile
                image.
            cell_size: Width and height of one maze cell in pixels.
            offset_x: Horizontal position of the maze origin in pixels.
            offset_y: Vertical position of the maze origin in pixels.

        Returns:
            None.
        """
        if cell_size not in self.walls:
            self.walls[cell_size] = self.load_walls(cell_size)
        x = cell_x * cell_size + offset_x
        y = cell_y * cell_size + offset_y

        self.draw_image(self.walls[cell_size][cell], x, y)

    def draw_circle(
        self,
        center_x: int,
        center_y: int,
        radius: int,
        color: tuple[int, int, int],
    ) -> None:
        """Fill a circle through clipped pixel writes.

        Args:
            center_x: Horizontal center of the circle in pixels.
            center_y: Vertical center of the circle in pixels.
            radius: Radius in pixels used for drawing or collision checks.
            color: RGB color for the pixels, outline or text.

        Returns:
            None.
        """
        for dy in range(-radius, radius + 1):
            half_width = isqrt(radius * radius - dy * dy)
            self.draw_horizontal_line(
                center_x - half_width, center_y + dy,
                center_x + half_width + 1, color,
            )

    def draw_text(
        self, text: str, x: int, y: int, size: int, color: Color,
        centre: bool = False, max_width: int | None = None,
    ) -> None:
        """Place pre-drawn bitmap glyphs, optionally centered and fitted.

        Args:
            text: Text to measure or render.
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            size: Requested font size in pixels.
            color: RGB color for the pixels, outline or text.
            centre: Whether x identifies the horizontal center instead of
                left edge.
            max_width: Maximum rendered text width; None disables fitting.

        Returns:
            None.
        """
        if not text:
            return
        if max_width is not None:
            size = min(size, max(1, 2 * max_width // len(text)))
        if centre:
            x -= self.measure_text(text, size)[0] // 2
        self.draw_image(self._text_image(text, size, color), x, y)

    def _text_image(
        self, text: str, size: int, color: Color
    ) -> pygame.Surface:
        """Copy existing BDF glyph bits into a cached text image.

        Args:
            text: Text to measure or render.
            size: Requested font size in pixels.
            color: RGB color for the pixels, outline or text.

        Returns:
            Cached transparent image containing the colored text mask.
        """
        key = (text, size, color)
        if key not in self.text_images:
            image = pygame.Surface(
                (max(1, len(text) * 10), 20), pygame.SRCALPHA,
            )
            for index, char in enumerate(text):
                if char not in self.glyph_pixels:
                    glyph = self.font.glyph(char) or self.font.glyph('?')
                    self.glyph_pixels[char] = cast(
                        list[list[int]], glyph.draw().todata(2),
                    )
                for y, row in enumerate(self.glyph_pixels[char]):
                    for x, bit in enumerate(row):
                        if bit:
                            image.set_at((index * 10 + x, y), color)
            image = self.scale_image(
                image, (
                    max(1, self.measure_text(text, size)[0]), max(1, size),
                ),
            )
            if len(self.text_images) >= 128:
                self.text_images.pop(next(iter(self.text_images)))
            self.text_images[key] = image
        return self.text_images[key]

    def clear(self, color: Color = (0, 0, 0)) -> None:
        """Replace all pixels on the drawing target with one color.

        Args:
            color: RGB color for the pixels, outline or text.

        Returns:
            None.
        """
        self.fill_rect(0, 0, *self.screen.get_size(), color)

    def draw_rect(
        self, x: int, y: int, width: int, height: int,
        color: Color, thickness: int = 1,
    ) -> None:
        """Draw the four edges of a rectangular outline.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.
            color: RGB color for the pixels, outline or text.
            thickness: Stroke width in pixels.

        Returns:
            None.
        """
        self.draw_vertical_line(x, y, y + height, color, thickness)
        self.draw_horizontal_line(x, y, x + width, color, thickness)
        self.draw_horizontal_line(x, y + height, x + width, color, thickness)
        self.draw_vertical_line(x + width, y, y + height, color, thickness)

    def measure_text(self, text: str, size: int) -> tuple[int, int]:
        """Measure the fixed-width bitmap font without rasterizing glyphs.

        Args:
            text: Text to measure or render.
            size: Requested font size in pixels.

        Returns:
            Width and height of the text in pixels.
        """
        return len(text) * max(1, size // 2), max(1, size)

    def fill_rect(
        self, x: int, y: int, width: int, height: int, color: Color
    ) -> None:
        """Fill a panel using the drawing target's pixel buffer.

        Args:
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.
            color: RGB color for the pixels, outline or text.

        Returns:
            None.
        """
        left, top = max(0, x), max(0, y)
        right = min(self.screen.get_width(), x + width)
        bottom = min(self.screen.get_height(), y + height)
        if right <= left or bottom <= top:
            return
        pixel = self.screen.map_rgb(color).to_bytes(
            self.screen.get_bytesize(), sys.byteorder,
        )
        row = pixel * (right - left)
        buffer = self.screen.get_buffer()
        pitch = self.screen.get_pitch()
        offset_x = left * self.screen.get_bytesize()
        for row_y in range(top, bottom):
            buffer.write(row, row_y * pitch + offset_x)

    @staticmethod
    def scale_image(
        image: pygame.Surface, size: tuple[int, int]
    ) -> pygame.Surface:
        """Resize an image, equivalent to Codam mlx_resize_image.

        Args:
            image: Prepared image to resize or place on the drawing target.
            size: Target width and height in pixels.

        Returns:
            New image with the requested width and height.
        """
        return pygame.transform.scale(image, size)

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        """Place a prepared image at a pixel position.

        Args:
            image: Prepared image to resize or place on the drawing target.
            x: Horizontal position in pixels.
            y: Vertical position in pixels.

        Returns:
            None.
        """
        self.screen.blit(image, (x, y))
