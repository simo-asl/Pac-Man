from pydantic import BaseModel, Field


class ConfigLevel(BaseModel):
    width: int = Field(default=39, ge=5)
    height: int = Field(default=29, ge=5)
    seed: int | None = None


class GameConfig(BaseModel):
    highscore_filename: str = "highscores.json"
    lives: int = Field(default=3, ge=1)
    pacgum: int = Field(default=42, ge=0)

    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)

    level_max_time: int = Field(default=90, ge=1)
    levels: list[ConfigLevel] = Field(
        default_factory=lambda: (
            [ConfigLevel(seed=42)] + [ConfigLevel() for _ in range(9)]
        )
    )
