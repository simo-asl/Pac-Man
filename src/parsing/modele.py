"""Define validated configuration fields and safe defaults."""

from pydantic import BaseModel, Field, ConfigDict


class ConfigLevel(BaseModel):
    """Define validated maze dimensions and optional seed."""

    model_config = ConfigDict(strict=True, extra="ignore")

    # The 2100x1800 window leaves a 1980x1380 play area: 32px minimum tiles.
    width: int = Field(default=39, ge=15, le=61)
    height: int = Field(default=29, ge=11, le=43)
    seed: int | None = None


class GameConfig(BaseModel):
    """Validated gameplay settings."""

    model_config = ConfigDict(strict=True, extra="ignore")

    highscore_filename: str = Field(default="highscores.json", min_length=1)
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=0)

    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)

    level_max_time: int = Field(default=90, ge=1)
    levels: list[ConfigLevel] = Field(
        min_length=10,
        default_factory=lambda: (
            [ConfigLevel(seed=42)] + [ConfigLevel() for _ in range(9)]
        ),
    )
