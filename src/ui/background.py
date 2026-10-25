"""A quiet arcade backdrop rendered directly at the window resolution."""

import pygame

from .draw import Draw


def background(draw: Draw) -> pygame.Surface:
    """Cache a full-resolution gradient with subtle maze-inspired corners.

    Args:
        draw: Drawing helper for the target surface.

    Returns:
        pygame.Surface: Prepared native-resolution background surface.
    """
    width, height = draw.screen.get_size()
    surface = pygame.Surface((width, height)).convert()
    for y in range(height):
        amount = y / max(1, height - 1)
        color = tuple(
            round(top * (1 - amount) + bottom * amount)
            for top, bottom in ((17, 8), (24, 13), (37, 23))
        )
        surface.fill(color, (0, y, width, 1))
    painter = Draw(surface)
    margin = min(width, height) // 30
    painter.draw_rect(
        margin,
        margin,
        width - 2 * margin,
        height - 2 * margin,
        (30, 42, 60),
        2,
    )
    step = margin
    # Reflected corner motifs stay outside the centered menu content.
    for x, y, dx, dy in (
        (margin, margin, 1, 1),
        (width - margin, margin, -1, 1),
        (margin, height - margin, 1, -1),
        (width - margin, height - margin, -1, -1),
    ):
        for index in (1, 2):
            corner_x = x + dx * step * index
            corner_y = y + dy * step * index
            end_x = corner_x + dx * step * 2
            end_y = corner_y + dy * step
            painter.draw_horizontal_line(
                min(corner_x, end_x),
                corner_y,
                max(corner_x, end_x),
                (43, 65, 94),
                3,
            )
            painter.draw_vertical_line(
                corner_x,
                min(corner_y, end_y),
                max(corner_y, end_y),
                (43, 65, 94),
                3,
            )
    return surface
