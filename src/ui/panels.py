"""Shared colors and simple panels for the keyboard-driven interface."""

import pygame

from .draw import Color, Draw

GOLD = (242, 199, 75)
TEXT = (237, 242, 249)
MUTED = (157, 172, 193)
LINE = (45, 58, 77)
PANEL = (17, 24, 36)
ERROR = (238, 111, 107)


def panel(draw: Draw, rect: pygame.Rect, color: Color = LINE) -> None:
    """Draw a solid surface with a thin, quiet border.

    Args:
        draw: Drawing helper for the target surface.
        rect: Pixel rectangle occupied by the panel or option.
        color: RGB color used for the text, line or border.

    Returns:
        None.
    """
    draw.screen.fill(PANEL, rect)
    draw.draw_rect(rect.x, rect.y, rect.width, rect.height, color, 2)


def choice(
    draw: Draw,
    rect: pygame.Rect,
    label: str,
    size: int,
    active: bool,
) -> None:
    """Show one option, highlighting only the keyboard selection.

    Args:
        draw: Drawing helper for the target surface.
        rect: Pixel rectangle occupied by the panel or option.
        label: Text displayed inside the option.
        size: Requested font size in pixels.
        active: Whether this option is the current keyboard selection.

    Returns:
        None.
    """
    panel(draw, rect, GOLD if active else LINE)
    if active:
        draw.screen.fill(GOLD, (rect.x, rect.y, 5, rect.height))
    text_height = draw.measure_text(label, size)[1]
    draw.draw_text(
        label,
        rect.centerx,
        rect.centery - text_height // 2,
        size,
        GOLD if active else TEXT,
        True,
        max_width=rect.width * 4 // 5,
    )


def result(
    draw: Draw,
    title: str,
    score: int,
    hint: str,
    color: Color = GOLD,
    message: str = "",
    score_label: str = "FINAL SCORE",
) -> None:
    """Show the same score hierarchy for wins, losses and level completion.

    Args:
        draw: Drawing helper for the target surface.
        title: Heading displayed at the top of the page or result card.
        score: Actual game score to display.
        hint: Keyboard action displayed for the current screen.
        color: RGB color used for the text, line or border.
        message: Optional congratulatory text below the result heading.
        score_label: Label distinguishing a final score from an in-progress
            score.

    Returns:
        None.
    """
    width, height = draw.screen.get_size()
    rect = pygame.Rect(width // 6, height // 4, width * 2 // 3, height // 2)
    panel(draw, rect, color)
    size = max(20, min(width // 35, height // 35))
    lines = (
        (title, 1, size * 2, color),
        (message, 3, size * 4 // 5, MUTED),
        (score_label, 4, size * 3 // 4, MUTED),
        (str(score), 5, size * 3, GOLD),
        (hint, 8, size, TEXT),
    )
    for text, row, font_size, text_color in lines:
        draw.draw_text(
            text,
            rect.centerx,
            rect.y + rect.height * row // 10,
            font_size,
            text_color,
            True,
            max_width=rect.width * 6 // 7,
        )


def pause(draw: Draw, selected: int) -> None:
    """Render two clear choices without changing pause behavior.

    Args:
        draw: Drawing helper for the target surface.
        selected: Zero-based index of the highlighted option.

    Returns:
        None.
    """
    width, height = draw.screen.get_size()
    rect = pygame.Rect(width // 5, height // 4, width * 3 // 5, height // 2)
    panel(draw, rect, GOLD)
    size = max(20, min(width // 35, height // 35))
    draw.draw_text(
        "PAUSED",
        rect.centerx,
        rect.y + rect.height // 9,
        size * 2,
        GOLD,
        True,
    )
    for index, label in enumerate(("RESUME", "MAIN MENU")):
        button = pygame.Rect(
            rect.x + rect.width // 8,
            rect.y + rect.height * (4 + index * 2) // 11,
            rect.width * 3 // 4,
            rect.height // 8,
        )
        choice(draw, button, label, size, index == selected)
    draw.draw_text(
        "UP / DOWN  SELECT    ENTER  CONFIRM",
        rect.centerx,
        rect.y + rect.height * 4 // 5,
        size * 2 // 3,
        MUTED,
        True,
    )
    draw.draw_text(
        "P / ESC  RESUME",
        rect.centerx,
        rect.y + rect.height * 9 // 10,
        size * 2 // 3,
        MUTED,
        True,
    )
