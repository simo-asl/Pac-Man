from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


class score(BaseModel):
    name: str
    score: int = Field(ge=0, strict=True)


class high_score(BaseModel):
    scores: list[score]


class High:
    """Manage persistent Pac-Man highscores."""

    def __init__(self, path_name: str) -> None:
        self.path = Path(path_name)

    def valid_name(self, name: str) -> bool:
        """Check whether a player name follows the subject rules."""
        if not isinstance(name, str):
            return False

        if not 1 <= len(name) <= 10:
            return False

        if not name.strip():
            return False

        for char in name:
            if not char.isascii() or not (char.isalnum() or char == " "):
                return False

        return True

    def score_value(self, player: score) -> int:
        """Return the score used for sorting."""
        return player.score

    def load_highscore(self) -> high_score:
        """Load highscores, handling missing or invalid files."""
        try:
            if not self.path.exists():
                return high_score(scores=[])

            data = self.path.read_text(encoding="utf-8")

            if not data.strip():
                return high_score(scores=[])

            loaded = high_score.model_validate_json(data)

            valid_scores = []

            for player in loaded.scores:
                if self.valid_name(player.name):
                    valid_scores.append(player)

            valid_scores.sort(key=self.score_value, reverse=True)

            return high_score(scores=valid_scores[:10])

        except (OSError, UnicodeError, ValidationError) as error:
            print(f"Error loading highscores: {error}")
            return high_score(scores=[])

    def save_highscore(self, data: high_score) -> bool:
        """Save highscores to a JSON file."""
        try:
            self.path.write_text(
                data.model_dump_json(indent=4),
                encoding="utf-8",
            )
            return True

        except OSError as error:
            print(f"Error saving highscores: {error}")
            return False

    def add_score(self, name: str, points: int) -> bool:
        """Add a valid score and keep only the top 10."""
        if not self.valid_name(name):
            return False

        if type(points) is not int or points < 0:
            return False

        data = self.load_highscore()

        data.scores.append(score(name=name, score=points))

        data.scores.sort(key=self.score_value, reverse=True)

        data.scores = data.scores[:10]

        return self.save_highscore(data)

    def get_top_scores(self) -> list[score]:
        """Return the top 10 highscores."""
        data = self.load_highscore()
        return data.scores
