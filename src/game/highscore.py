import json

from parsing import GameConfig


def load_high_score(game_config: GameConfig) -> dict:
    with open(game_config.highscore_filename, "r+") as f:
        high_score = json.load(f)
    return high_score


def write_new_high(game_config: GameConfig, high_score: dict[str, int]) -> None:
    with open(game_config.highscore_filename, "w+") as f:
        json.dump(high_score, f)
