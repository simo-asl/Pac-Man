"""Read commented JSON and recover invalid settings independently."""

from pathlib import Path
from typing import Any

import hjson
from pydantic import BaseModel, ValidationError

from .modele import ConfigLevel, GameConfig


class Parser:
    """Load configuration without discarding valid sibling fields."""

    def __init__(self, file_path: str) -> None:
        """Initialize this object and its runtime dependencies.

        Args:
            file_path: User-supplied path to the JSON configuration file.

        Returns:
            None.
        """
        self.file_path = Path(file_path)

    def _fields(
        self, model: type[BaseModel], values: dict[str, Any], label: str
    ) -> dict[str, Any]:
        """Replace missing or invalid known fields with their defaults.

        Args:
            model: Pydantic model that defines valid fields and their
                defaults.
            values: Decoded configuration fields to validate independently.
            label: Prefix identifying this object in configuration
                warnings.

        Returns:
            Known fields with invalid or missing values replaced by
            defaults.
        """
        defaults = model().model_dump()
        selected = {key: value for key, value in values.items()
                    if key in model.model_fields}
        for key, default in defaults.items():
            if key not in selected:
                print(f"Config: {label}{key} missing; using {default!r}")
                selected[key] = default
        try:
            model.model_validate(selected)
        except ValidationError as error:
            for detail in error.errors():
                key = str(detail['loc'][0])
                print(f"Config: invalid {label}{key}; "
                      f"using {defaults[key]!r}")
                selected[key] = defaults[key]
        return selected

    def parser(self) -> GameConfig:
        """Return a usable config and report file or value errors clearly.

        Returns:
            Validated configuration, with safe defaults for unusable
            values.
        """
        try:
            if self.file_path.suffix.lower() != '.json':
                raise ValueError("Configuration filename must end in .json")
            text = self.file_path.read_text(encoding='utf-8')
            values = hjson.loads(text)
            if not isinstance(values, dict):
                raise ValueError("Configuration must be a JSON object")
        except (OSError, UnicodeError, ValueError, RecursionError,
                IndexError) as error:
            print(f"Config: {self.file_path}: {error}; using defaults")
            return GameConfig()

        raw_levels = values.get('levels')
        if isinstance(raw_levels, list) and raw_levels:
            levels = []
            for index, level in enumerate(raw_levels[:100]):
                if not isinstance(level, dict):
                    print(f"Config: invalid levels[{index}]; using defaults")
                    level = {}
                fields = self._fields(ConfigLevel, level, f'levels[{index}].')
                levels.append(ConfigLevel.model_validate(fields))
            if len(levels) < 10:
                print("Config: at least 10 levels required; adding defaults")
                levels.extend(ConfigLevel() for _ in range(10 - len(levels)))
            if len(raw_levels) > 100:
                print("Config: limiting levels to 100")
            values['levels'] = levels
        elif 'levels' in values:
            print("Config: invalid levels; using 10 default levels")
            values['levels'] = GameConfig().levels
        filename = values.get('highscore_filename')
        if isinstance(filename, str) and (
            not filename.strip() or '\x00' in filename
        ):
            print("Config: invalid highscore_filename; using highscores.json")
            values['highscore_filename'] = 'highscores.json'
        return GameConfig.model_validate(self._fields(GameConfig, values, ''))
