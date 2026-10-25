"""Validated settings and safe defaults for a playable game."""

from pydantic import BaseModel, Field, field_validator

MIN_LEVELS = 10
MAX_LEVELS = 100


class ConfigLevel(BaseModel):
    """Bound maze dimensions so every tile fits in the game window."""

    width: int = Field(default=39, ge=5, le=100, strict=True)
    height: int = Field(default=29, ge=5, le=70, strict=True)
    seed: int | None = Field(default=None, ge=1, strict=True)


def create_default_levels() -> list[ConfigLevel]:
    """Create independent settings for the default ten-level game.

    Returns:
        A fixed-seed first level followed by randomly seeded levels.
    """
    levels = [ConfigLevel(seed=42)]
    while len(levels) < MIN_LEVELS:
        levels.append(ConfigLevel())
    return levels


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
        default_factory=create_default_levels,
        min_length=MIN_LEVELS,
        max_length=MAX_LEVELS,
    )

    @field_validator('highscore_filename')
    @classmethod
    def validate_highscore_filename(cls, filename: str) -> str:
        """Reject paths that cannot name a highscore file.

        Args:
            filename: Highscore destination supplied in the configuration.

        Returns:
            The original valid destination path.

        Raises:
            ValueError: The path is blank or contains a null byte.
        """
        if not filename.strip() or '\x00' in filename:
            raise ValueError('Filename must be nonblank and contain no nulls')
        return filename
