"""Validated settings and safe defaults for a playable game."""

from pydantic import BaseModel, Field


class ConfigLevel(BaseModel):
    """Bound maze dimensions so every tile fits in the game window."""

    width: int = Field(default=39, ge=5, le=100, strict=True)
    height: int = Field(default=29, ge=5, le=70, strict=True)
    seed: int | None = Field(default=None, strict=True)


class GameConfig(BaseModel):
    """Store gameplay settings; unknown configuration keys are ignored."""

    highscore_filename: str = Field(default="highscores.json", min_length=1)
    lives: int = Field(default=3, ge=1, strict=True)
    pacgum: int = Field(default=42, ge=0, strict=True)
    points_per_pacgum: int = Field(default=10, ge=0, strict=True)
    points_per_super_pacgum: int = Field(default=50, ge=0, strict=True)
    points_per_ghost: int = Field(default=200, ge=0, strict=True)
    level_max_time: int = Field(default=90, ge=1, strict=True)
    levels: list[ConfigLevel] = Field(
        default_factory=lambda: (
            [ConfigLevel(seed=42)] + [ConfigLevel() for _ in range(9)]
        ),
        min_length=10,
        max_length=100,
    )
