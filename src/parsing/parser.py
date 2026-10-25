"""Read JSON configuration with full-line comments and safe defaults."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from .modele import ConfigLevel, GameConfig


class Parser:
    """Validate each setting independently, preserving valid user choices."""

    def __init__(self, file_path: str) -> None:
        """Remember the configuration path.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            None.
        """
        self.file_path = Path(file_path)

    def _remove_comments(self, text: str) -> str:
        """Ignore full lines beginning with # or //; leave strings intact.

        Args:
            text: Text to measure, render or process.

        Returns:
            str: JSON text without supported full-line comments.
        """
        return "\n".join(
            line
            for line in text.splitlines()
            if not line.lstrip().startswith(("#", "//"))
        )

    def _validate_fields(
        self, model: type[BaseModel], values: dict[str, Any]
    ) -> dict[str, Any]:
        """Replace only invalid known fields with their model defaults.

        Args:
            model: Pydantic model supplying defaults and validation rules.
            values: Parsed configuration values to validate independently.

        Returns:
            dict[str, Any]: Validated known values with invalid fields set to
                defaults.
        """
        defaults = model().model_dump()
        result = {
            key: value
            for key, value in values.items()
            if key in model.model_fields
        }
        for key in defaults:
            if key not in result and defaults[key] is not None:
                print(f"Config: {key} missing; using its default.")
        try:
            return model.model_validate(result).model_dump()
        except ValidationError as error:
            for issue in error.errors():
                key = str(issue["loc"][0])
                print(f"Config: invalid {key}; using its default.")
                result[key] = defaults[key]
            return model.model_validate(result).model_dump()

    def parser(self) -> GameConfig:
        """Load a JSON file; report file/syntax errors without a traceback.

        Returns:
            GameConfig: Configuration with safe defaults and validated level
                settings.

        Raises:
            ValueError: The file cannot be read or does not contain a JSON
                object.
        """
        if self.file_path.suffix.lower() != ".json":
            raise ValueError("Configuration filename must end in .json")
        try:
            text = self.file_path.read_text(encoding="utf-8")
            values = json.loads(self._remove_comments(text))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError(f"Cannot read configuration: {error}") from error
        if not isinstance(values, dict):
            raise ValueError("Configuration must be a JSON object")
        levels = values.get("levels")
        if isinstance(levels, list):
            validated_levels = []
            for index, level in enumerate(levels):
                if not isinstance(level, dict):
                    print(f"Config: level {index + 1} must be an object; "
                          "using defaults.")
                    level = {}
                validated_levels.append(
                    self._validate_fields(ConfigLevel, level)
                )
            values["levels"] = validated_levels
        return GameConfig.model_validate(
            self._validate_fields(GameConfig, values)
        )
