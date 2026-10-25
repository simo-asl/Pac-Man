"""Render the interface using MLX-style image and pixel operations."""

import sys
from math import isqrt
from typing import cast

from bdfparser import Font

import pygame

from ..resources import resource_path

Color = tuple[int, int, int]
FONT_GLYPH_WIDTH = 10
FONT_GLYPH_HEIGHT = 20
TEXT_CACHE_LIMIT = 128


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
        self.wall_tile_cache: dict[int, dict[int, pygame.Surface]] = {}
        font_path = resource_path('assets/fonts/Tamzen10x20b.bdf')
        self.font = Font(str(font_path))
        self.glyph_bitmap_cache: dict[str, list[list[int]]] = {}
        self.text_image_cache: dict[
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
        for wall_mask in range(16):
            walls[wall_mask] = self.load_image(
                f"assets/walls/{wall_mask}.png",
                (cell_size, cell_size),
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
        if cell_size not in self.wall_tile_cache:
            self.wall_tile_cache[cell_size] = self.load_walls(cell_size)
        x = cell_x * cell_size + offset_x
        y = cell_y * cell_size + offset_y

        self.draw_image(self.wall_tile_cache[cell_size][cell], x, y)

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
        for row_offset in range(-radius, radius + 1):
            half_width = isqrt(radius * radius - row_offset * row_offset)
            self.draw_horizontal_line(
                center_x - half_width, center_y + row_offset,
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
            fitted_size = (
                FONT_GLYPH_HEIGHT * max_width // (len(text) * FONT_GLYPH_WIDTH)
            )
            size = min(size, max(1, fitted_size))
        if centre:
            x -= self.measure_text(text, size)[0] // 2
        self.draw_image(self._text_image(text, size, color), x, y)

    def _text_image(
        self, text: str, size: int, color: Color
    ) -> pygame.Surface:
        """Return a cached sized text image, preparing it when needed.

        Args:
            text: Text to measure or render.
            size: Requested font size in pixels.
            color: RGB color for the pixels, outline or text.

        Returns:
            Cached transparent image containing the colored text mask.
        """
        cache_key = (text, size, color)
        if cache_key not in self.text_image_cache:
            text_image = self._compose_text(text, color)
            text_width, text_height = self.measure_text(text, size)
            if len(self.text_image_cache) >= TEXT_CACHE_LIMIT:
                oldest_key = next(iter(self.text_image_cache))
                self.text_image_cache.pop(oldest_key)
            self.text_image_cache[cache_key] = self.scale_image(
                text_image, (max(1, text_width), text_height),
            )
        return self.text_image_cache[cache_key]

    def _glyph_bitmap(self, character: str) -> list[list[int]]:
        """Load and cache one pre-drawn glyph through bdfparser.

        Args:
            character: Character to load, with '?' used when unavailable.

        Returns:
            Rows of binary pixel values from the bundled bitmap font.
        """
        if character not in self.glyph_bitmap_cache:
            glyph = self.font.glyph(character) or self.font.glyph('?')
            self.glyph_bitmap_cache[character] = cast(
                list[list[int]], glyph.draw().todata(2),
            )
        return self.glyph_bitmap_cache[character]

    def _compose_text(self, text: str, color: Color) -> pygame.Surface:
        """Copy existing glyph pixels into a native-size text image.

        Args:
            text: Characters to arrange from left to right.
            color: RGB color for the glyph's set pixels.

        Returns:
            Transparent text image before resizing or placement.
        """
        text_image = pygame.Surface(
            (max(1, len(text) * FONT_GLYPH_WIDTH), FONT_GLYPH_HEIGHT),
            pygame.SRCALPHA,
        )
        for character_index, character in enumerate(text):
            glyph_origin_x = character_index * FONT_GLYPH_WIDTH
            glyph_rows = self._glyph_bitmap(character)
            for pixel_y, bitmap_row in enumerate(glyph_rows):
                for pixel_x, is_set in enumerate(bitmap_row):
                    if is_set:
                        text_image.set_at(
                            (glyph_origin_x + pixel_x, pixel_y), color,
                        )
        return text_image

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
        glyph_width = max(1, size * FONT_GLYPH_WIDTH // FONT_GLYPH_HEIGHT)
        text_width = len(text) * glyph_width
        text_height = max(1, size)
        return text_width, text_height

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
        bytes_per_pixel = self.screen.get_bytesize()
        mapped_color = self.screen.map_rgb(color)
        pixel_bytes = mapped_color.to_bytes(bytes_per_pixel, sys.byteorder)
        row_bytes = pixel_bytes * (right - left)
        pixel_buffer = self.screen.get_buffer()
        row_stride = self.screen.get_pitch()
        offset_x = left * bytes_per_pixel
        for row_y in range(top, bottom):
            row_offset = row_y * row_stride + offset_x
            pixel_buffer.write(row_bytes, row_offset)

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
