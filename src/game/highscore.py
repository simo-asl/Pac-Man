"""Validate, rank and persist the top ten highscores."""

from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


class score(BaseModel):
    """Validate a player name and a nonnegative integer score.
    """
    name: str
    score: int = Field(ge=0, strict=True)


class high_score(BaseModel):
    """Validate the collection stored in a highscore JSON file.
    """
    scores: list[score]


class High:
    """Manage persistent Pac-Man highscores."""

    def __init__(self, path_name: str) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            path_name: Filename used to load and save the highscore JSON
                document.

        Returns:
            None.
        """
        self.path = Path(path_name)

    def valid_name(self, name: str) -> bool:
        """Check whether a player name follows the subject rules.

        Args:
            name: Player name limited to ten ASCII letters, digits or
                spaces.

        Returns:
            True if the name satisfies length and character restrictions.
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
            player: Saved highscore entry whose score is used for sorting.

        Returns:
            Nonnegative score used for descending ranking.
        """
        return player.score

    def load_highscore(self) -> high_score:
        """Load highscores, handling missing or invalid files.

        Returns:
            Top ten valid entries, or an empty collection on file errors.
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
            data: Validated highscore collection to write to disk.

        Returns:
            True if writing succeeded; False if the file cannot be written.
        """
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
        """Increase the current score by the supplied point amount.

        Args:
            name: Player name limited to ten ASCII letters, digits or
                spaces.
            points: Nonnegative score value awarded for this item or game.

        Returns:
            True if the name and score were accepted and the file was
            saved.
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
            Up to ten saved entries ordered from highest to lowest score.
        """
        data = self.load_highscore()
        return data.scores
