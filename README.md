*This project has been created as part of the 42 curriculum by tlaghzal, mel-asla.*

# Pac-Man

## Description

A configurable Pac-Man game using Pygame, Tamzen bitmap lettering, Pydantic,
Hjson and the assigned MazeGenerator package.

## Instructions

Install Python 3.12 or later and uv, then run:

```sh
make install
make run
# Equivalent commands after activating .venv:
python3 pac-man.py config.json
pac-man config.json
python3 -m src config.json
```

The window is restored to 1800×1200. Actor sprites scale to the maze tiles.
Losing a life displays a short LIFE LOST message; game over shows the cause
and final score before name entry. Ghosts follow open paths around walls,
flee while edible, and respawn after five seconds.

Use `make debug` for pdb, `make lint` for Flake8 and the subject's Mypy checks,
and `make clean` to remove generated caches. Set `ARGS=other.json` to select
another configuration. The console entry point is `src.__main__:main`.

## Current game controls

Run `.venv/bin/python -m src config.json` after installing dependencies.
Use Up/Down and Enter in menus, arrow keys to move, and P or Escape to
pause/resume. The pause menu offers Resume, Instructions and Main Menu. Instructions keep
the game paused; Enter or Escape returns to the pause choices. Eat all pellets before
the timer expires; completing all levels opens the victory screen. Both a win
and a loss lead to name entry, score saving, then the main menu. Names accept
1–10 ASCII letters, digits and spaces and must contain a non-space character.
Save failures leave name entry open so you can fix the destination and retry.
Cheats: I toggles invincibility, F freezes ghosts, L adds a life, S skips a level.

## Configuration and recovery

The configuration is a JSON object. Comments beginning with `#` or `//` and
`/* ... */` blocks are supported outside quoted strings. Unknown keys are
ignored. Missing or invalid fields produce a console message and use their
own default, preserving other valid settings. Unreadable or malformed files
use the complete default configuration.

| Key | Default | Accepted values |
| --- | --- | --- |
| `highscore_filename` | `highscores.json` | Nonempty file path |
| `lives` | 3 | Integer ≥ 1 |
| `pacgum` | 42 | Integer ≥ 0; at least 70% of corridors receive pellets |
| `points_per_pacgum` | 10 | Integer ≥ 0 |
| `points_per_super_pacgum` | 50 | Integer ≥ 0 |
| `points_per_ghost` | 200 | Integer ≥ 0 |
| `level_max_time` | 90 | Integer seconds ≥ 1 |
| `levels` | 10 levels | Array of level objects; short arrays are padded to 10 |
| `levels[].width` | 39 | Integer 5–100 |
| `levels[].height` | 29 | Integer 5–70 |
| `levels[].seed` | `null` | Integer or `null` |

The first level defaults to seed 42; subsequent levels use the generator's
random seed unless configured. Explicit seeds are respected. At most 100 levels
are loaded. Dimension limits keep tiles visible in the fixed game window.
Highscores load when the menu starts and save to `highscore_filename` at game
end; the top ten appear in the Highscores page. The assigned generator is used
with `perfect=False`; generation failures return to the menu with feedback.

## Rendering libraries

Pygame handles the window, events, images and pixel buffers. `Draw` owns
rendering, including actor sprites and text. The `bdfparser` library reads the
bundled Tamzen Bold 10×20 BDF font, whose glyphs are already drawn as bitmaps.
The game copies those existing bits into cached images and resizes them;
it never rasterizes a TrueType font. Pillow and Pygame's font API are unused.
Hjson parses commented configuration and Pydantic validates its fields.

The graphics API comparison is documented in [MLX.md](MLX.md).
The font and its license are bundled under `src/assets/fonts/`.

## Resources

- [42 Paris MiniLibX API](https://github.com/42Paris/minilibx-linux/blob/master/mlx.h)
- [Codam MLX42 API](https://github.com/codam-coding-college/MLX42/blob/master/include/MLX42/MLX42.h)
- [bdfparser](https://github.com/tomchen/bdfparser)
- [Tamzen bitmap font](https://github.com/sunaku/tamzen-font)
- [Hjson syntax](https://hjson.github.io/syntax.html)
- [Pydantic](https://docs.pydantic.dev/)

AI assisted with UI and parser fixes, API comparison, docstrings, installation
configuration and regression checks. Team members must review these changes.
