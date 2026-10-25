"""Load commented JSON, validate settings, and recover invalid fields."""

from pathlib import Path
from typing import Any, TypeVar

import hjson
from pydantic import BaseModel, ValidationError

from .models import MAX_LEVELS, MIN_LEVELS, ConfigLevel, GameConfig

ConfigModel = TypeVar('ConfigModel', bound=BaseModel)


class Parser:
    """Coordinate configuration loading without discarding valid fields."""

    def __init__(self, file_path: str) -> None:
        """Store the configuration file location.

        Args:
            file_path: Path to the commented JSON configuration.

        Returns:
            None.
        """
        self.file_path = Path(file_path)

    def _read_config(self) -> dict[str, Any]:
        """Decode one configuration object using Hjson.

        Returns:
            Raw settings before validation or default recovery.

        Raises:
            OSError: The configuration file cannot be read.
            UnicodeError: The file is not valid UTF-8.
            ValueError: The extension, syntax, or root object is invalid.
            IndexError: Hjson encounters an unterminated block comment.
            RecursionError: The configuration is nested too deeply.
        """
        if self.file_path.suffix.lower() != '.json':
            raise ValueError('Configuration filename must end in .json')
        file_contents = self.file_path.read_text(encoding='utf-8')
        settings = hjson.loads(file_contents)
        if not isinstance(settings, dict):
            raise ValueError('Configuration must be a JSON object')
        return settings

    def _validate_fields(
        self, model_type: type[ConfigModel], settings: dict[str, Any],
        field_prefix: str = '',
    ) -> ConfigModel:
        """Validate known fields and replace unusable ones with defaults.

        Args:
            model_type: Pydantic model defining accepted fields and defaults.
            settings: Raw values for this configuration object.
            field_prefix: Location prefix used in validation messages.

        Returns:
            Validated model retaining every valid supplied field.
        """
        defaults = model_type()
        for field_name in model_type.model_fields:
            if field_name not in settings:
                print(f'Config: {field_prefix}{field_name} missing; '
                      'using default')
        try:
            return model_type.model_validate(settings)
        except ValidationError as error:
            repaired_settings = settings.copy()
            for issue in error.errors():
                field_name = str(issue['loc'][0])
                print(f'Config: invalid {field_prefix}{field_name}: '
                      f'{issue["msg"]}; using default')
                repaired_settings[field_name] = getattr(defaults, field_name)
            return model_type.model_validate(repaired_settings)

    def _parse_levels(self, raw_levels: Any) -> list[ConfigLevel]:
        """Normalize level entries and enforce the supported level count.

        Args:
            raw_levels: Decoded level value; invalid containers use defaults.

        Returns:
            Between ten and one hundred validated level configurations.
        """
        if not isinstance(raw_levels, list) or not raw_levels:
            print('Config: invalid levels; using default levels')
            return GameConfig().levels
        levels = []
        for level_index, level_settings in enumerate(raw_levels[:MAX_LEVELS]):
            if not isinstance(level_settings, dict):
                print(f'Config: invalid levels[{level_index}]; using defaults')
                level_settings = {}
            levels.append(self._validate_fields(
                ConfigLevel, level_settings, f'levels[{level_index}].',
            ))
        if len(levels) < MIN_LEVELS:
            print(f'Config: at least {MIN_LEVELS} levels required; '
                  'adding defaults')
            levels.extend(
                ConfigLevel() for _ in range(MIN_LEVELS - len(levels))
            )
        if len(raw_levels) > MAX_LEVELS:
            print(f'Config: limiting levels to {MAX_LEVELS}')
        return levels

    def parse(self) -> GameConfig:
        """Load, normalize, and validate the complete configuration.

        Returns:
            Usable settings, or full defaults when the file cannot be read.
        """
        try:
            settings = self._read_config()
        except (OSError, UnicodeError, ValueError, RecursionError,
                IndexError) as error:
            print(f'Config: {self.file_path}: {error}; using defaults')
            return GameConfig()
        if 'levels' in settings:
            settings['levels'] = self._parse_levels(settings['levels'])
        return self._validate_fields(GameConfig, settings)
