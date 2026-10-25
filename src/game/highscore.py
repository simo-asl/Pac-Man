"""Validate and persist the ten highest named scores."""

from pathlib import Path
from tempfile import NamedTemporaryFile

from pydantic import BaseModel, Field, ValidationError


class score(BaseModel):
    """Validate a named non-negative score."""

    name: str
    score: int = Field(ge=0, strict=True)


class high_score(BaseModel):
    """Represent the stored high-score list."""

    scores: list[score]


class High:
    """Manage persistent Pac-Man highscores."""

    def __init__(self, path_name: str) -> None:
        """Initialize this object and its dependencies.

        Args:
            path_name: Path to the persistent high-score JSON file.

        Returns:
            None.
        """
        self.path = Path(path_name)

    def valid_name(self, name: str) -> bool:
        """Check whether a player name follows the subject rules.

        Args:
            name: Player name to validate, display or save.

        Returns:
            bool: True for a nonempty permitted name of at most ten characters.
        """
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
        """Return the score used for sorting.

        Args:
            player: Validated saved score entry to compare.

        Returns:
            int: The points used to sort this saved entry.
        """
        return player.score

    def load_highscore(self) -> high_score:
        """Load highscores, handling missing or invalid files.

        Returns:
            high_score: Validated and sorted score data, or an empty list on
                file errors.
        """
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
            print(f"Warning: Cannot load highscores: {error}")
            return high_score(scores=[])

    def save_highscore(self, data: high_score) -> bool:
        """Save highscores to a JSON file.

        Args:
            data: Validated high-score data to persist.

        Returns:
            bool: True after successful replacement, or False after a file
                error.
        """
        temporary: Path | None = None
        try:
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=self.path.name + ".",
                suffix=".tmp",
                delete=False,
            ) as output:
                temporary = Path(output.name)
                output.write(data.model_dump_json(indent=4))
            temporary.replace(self.path)
            return True
        except OSError as error:
            print(f"Error saving highscores: {error}")
            return False
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError:
                    pass

    def add_score(self, name: str, points: int) -> bool:
        """Add a valid score and keep only the top 10.

        Args:
            name: Player name to validate, display or save.
            points: Non-negative number of points awarded or stored.

        Returns:
            bool: True if the valid name and points were saved successfully.
        """
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
        """Return the top 10 highscores.

        Returns:
            list[score]: At most ten valid entries sorted by descending points.
        """
        data = self.load_highscore()
        return data.scores
